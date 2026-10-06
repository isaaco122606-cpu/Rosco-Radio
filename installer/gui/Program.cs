using System.Diagnostics;
using System.IO.Compression;
using System.Security.Cryptography;
using System.Text.Json;
using System.Windows.Forms;

namespace RoscoRadio.Setup;

internal static class Program
{
    [STAThread]
    static void Main()
    {
        ApplicationConfiguration.Initialize();
        Application.Run(new InstallerForm());
    }
}

internal sealed class InstallerForm : Form
{
    const string Server = "https://nexusupdater.duckdns.org";
    const string AppId = "rosco-radio";

    readonly ComboBox channel = new() { DropDownStyle = ComboBoxStyle.DropDownList };
    readonly Button install = new() { Text = "Install Rosco Radio", Height = 42 };
    readonly ProgressBar progress = new() { Style = ProgressBarStyle.Marquee, Visible = false, Height = 18 };
    readonly Label status = new() { AutoSize = false, Height = 70, Text = "Ready to install Rosco Radio." };
    readonly CheckBox launch = new() { Text = "Launch Rosco Radio when finished", Checked = true, AutoSize = true };

    public InstallerForm()
    {
        Text = "Rosco Radio Setup";
        Width = 540;
        Height = 330;
        StartPosition = FormStartPosition.CenterScreen;
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MaximizeBox = false;

        channel.Items.AddRange(new object[] { "Stable", "Beta" });
        channel.SelectedIndex = 0;

        var title = new Label
        {
            Text = "Rosco Radio",
            Font = new Font(Font.FontFamily, 22, FontStyle.Bold),
            AutoSize = true
        };
        var subtitle = new Label
        {
            Text = "Online Installer powered by NexusUpdater",
            AutoSize = true
        };
        var channelLabel = new Label { Text = "Release channel", AutoSize = true };

        var panel = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            Padding = new Padding(24),
            RowCount = 8,
            ColumnCount = 1
        };
        panel.RowStyles.Clear();
        for (int i = 0; i < 8; i++) panel.RowStyles.Add(new RowStyle(SizeType.AutoSize));
        panel.Controls.Add(title);
        panel.Controls.Add(subtitle);
        panel.Controls.Add(new Label { Height = 12 });
        panel.Controls.Add(channelLabel);
        panel.Controls.Add(channel);
        panel.Controls.Add(launch);
        panel.Controls.Add(install);
        panel.Controls.Add(progress);
        panel.Controls.Add(status);
        Controls.Add(panel);

        install.Click += async (_, _) => await InstallAsync();
    }

    async Task InstallAsync()
    {
        install.Enabled = false;
        channel.Enabled = false;
        progress.Visible = true;
        UseWaitCursor = true;

        try
        {
            string selected = channel.SelectedIndex == 1 ? "beta" : "stable";
            SetStatus($"Contacting NexusUpdater ({selected})...");

            using var http = new HttpClient();
            http.DefaultRequestHeaders.UserAgent.ParseAdd("RoscoRadio-Setup/0.1");

            string manifestUrl = $"{Server}/api/v1/apps/{AppId}/manifest?channel={selected}";
            string json = await http.GetStringAsync(manifestUrl);
            using var doc = JsonDocument.Parse(json);
            var root = doc.RootElement;
            string version = root.GetProperty("version").GetString() ?? throw new Exception("Manifest is missing version.");
            string packageUrl = root.GetProperty("package_url").GetString() ?? throw new Exception("Manifest is missing package URL.");
            string expectedHash = (root.GetProperty("sha256").GetString() ?? throw new Exception("Manifest is missing SHA-256.")).Trim().ToLowerInvariant();

            if (!Uri.TryCreate(packageUrl, UriKind.Absolute, out var uri) || uri.Scheme != Uri.UriSchemeHttps)
                throw new Exception("NexusUpdater returned an invalid package URL.");

            string documents = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            string updates = Path.Combine(documents, "Rosco Radio", "Updates");
            string downloads = Path.Combine(updates, "Downloads");
            string staging = Path.Combine(updates, "Staging", "OnlineInstaller");
            string backups = Path.Combine(updates, "Backup");
            string installDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Programs", "RoscoRadio");
            Directory.CreateDirectory(downloads);
            Directory.CreateDirectory(backups);

            string zipPath = Path.Combine(downloads, $"RoscoRadio-v{version}.zip");
            string partial = zipPath + ".part";
            if (File.Exists(partial)) File.Delete(partial);

            SetStatus($"Downloading Rosco Radio v{version}...");
            await using (var source = await http.GetStreamAsync(uri))
            await using (var dest = File.Create(partial))
                await source.CopyToAsync(dest);

            SetStatus("Verifying SHA-256...");
            string actualHash;
            using (var stream = File.OpenRead(partial))
                actualHash = Convert.ToHexString(SHA256.HashData(stream)).ToLowerInvariant();
            if (actualHash != expectedHash)
            {
                File.Delete(partial);
                throw new Exception("Package verification failed. The downloaded file did not match NexusUpdater's SHA-256.");
            }
            File.Move(partial, zipPath, true);

            SetStatus("Preparing installation...");
            if (Directory.Exists(staging)) Directory.Delete(staging, true);
            Directory.CreateDirectory(staging);
            ZipFile.ExtractToDirectory(zipPath, staging, true);

            string sourceDir = staging;
            var dirs = Directory.GetDirectories(staging);
            var files = Directory.GetFiles(staging);
            if (dirs.Length == 1 && files.Length == 0) sourceDir = dirs[0];

            if (Directory.Exists(installDir))
            {
                string backup = Path.Combine(backups, "OnlineInstaller-" + DateTime.Now.ToString("yyyyMMdd-HHmmss"));
                CopyDirectory(installDir, backup);
                Directory.Delete(installDir, true);
            }

            Directory.CreateDirectory(installDir);
            CopyDirectory(sourceDir, installDir);
            Directory.Delete(staging, true);

            string runBat = Path.Combine(installDir, "run.bat");
            if (!File.Exists(runBat)) throw new Exception("Installation completed, but run.bat was not found.");

            // Simple current-user desktop launcher that does not require admin rights.
            try
            {
                string desktop = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
                string cmd = Path.Combine(desktop, "Rosco Radio.cmd");
                File.WriteAllText(cmd, $"@echo off\r\ncd /d \"{installDir}\"\r\ncall \"{runBat}\"\r\n");
            }
            catch { }

            progress.Visible = false;
            UseWaitCursor = false;
            SetStatus($"Rosco Radio v{version} installed successfully.\n{installDir}");
            install.Text = "Installed";

            if (launch.Checked)
                Process.Start(new ProcessStartInfo(runBat) { WorkingDirectory = installDir, UseShellExecute = true });

            MessageBox.Show(this, $"Rosco Radio v{version} is installed and ready.", "Rosco Radio Setup", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            progress.Visible = false;
            UseWaitCursor = false;
            install.Enabled = true;
            channel.Enabled = true;
            SetStatus("Installation failed: " + ex.Message);
            MessageBox.Show(this, ex.Message, "Rosco Radio installation failed", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }

    void SetStatus(string text)
    {
        if (InvokeRequired) { BeginInvoke(() => SetStatus(text)); return; }
        status.Text = text;
        status.Refresh();
    }

    static void CopyDirectory(string source, string destination)
    {
        Directory.CreateDirectory(destination);
        foreach (string file in Directory.GetFiles(source))
            File.Copy(file, Path.Combine(destination, Path.GetFileName(file)), true);
        foreach (string dir in Directory.GetDirectories(source))
            CopyDirectory(dir, Path.Combine(destination, Path.GetFileName(dir)));
    }
}
