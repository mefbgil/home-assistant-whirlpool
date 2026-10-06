# Whirlpool Appliances for Home Assistant

Custom Home Assistant integration for Whirlpool appliances, based on the
Whirlpool integration included with Home Assistant Core.

This version adds AWS IoT refrigerator support, including support developed
and tested with the Whirlpool WRFC7036RZ refrigerator.

## Refrigerator support

The refrigerator implementation is intentionally read-only. It exposes
available appliance state to Home Assistant but does not provide controls
that can change refrigerator settings.

Depending on appliance capabilities, entities include:

- Refrigerator temperature
- Freezer temperature
- Pantry mode
- Refrigerator, freezer, and pantry door states
- Freezer and icebox ice-maker states
- Max Cool and Max Ice status
- Vacation mode
- Control lock
- Sabbath mode
- Quiet mode
- Water-filter status
- Ice type
- Door alarm
- Power-outage alarms

## Installation

Install through HACS as a custom integration repository.

This custom component uses the same `whirlpool` domain as the Whirlpool
integration included with Home Assistant Core and therefore overrides the
built-in integration while installed.

Restart Home Assistant after installation or updating.

## Library

AWS IoT refrigerator support is provided by a patched version of
`whirlpool-sixth-sense` maintained in the companion GitHub repository:

`mefbgil/whirlpool-sixth-sense`

The dependency is pinned by the integration manifest to a tested revision.

## License

This repository contains code derived from the Whirlpool integration in
Home Assistant Core. See the source files and upstream projects for
applicable licensing and attribution.
