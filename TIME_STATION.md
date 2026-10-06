# Rosco Radio Time Station — Beta

The Beta Time Station workspace provides guided setup and scheduled ten-minute station-identification audio using the Local Radio TX output. VOX is the default transmit method.

## Setup tree

1. Are you licensed?
2. Do you have a Baofeng or another radio/interface using the conventional K1 two-plug audio/PTT connector?
3. Confirm the computer clock is synchronized.
4. Choose Local time or UTC.
5. Enter service, callsign, frequency, and the station owner's question email.
6. Confirm operator responsibility before scheduled RF can be armed.

## Ten-minute station ID

RR generates this text from the configured profile:

`[CALLSIGN], hosted on [FREQUENCY], made possible by RoscoRadio.`

`https://github.com/isaaco122606-cpu/Rosco-Radio.`

`For more information, email [STATION OWNER'S QUESTION EMAIL] or roscosponsorships@gmail.com.`

## Service behavior

- Amateur Radio (Ham): scheduled VOX can be armed only after setup/licensing/clock/operator confirmations are complete.
- GMRS: recurring one-way Time Station RF is preview-only in this Beta. Local audio preview remains available.

The licensed control operator remains responsible for permitted content, frequency/channel selection, interference avoidance, and compliance with applicable rules.
