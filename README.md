# ideapad-perf
Battery manager to handle system performance modes and charge modes through acpi calls (for some AMD models of Lenovo IdeaPad) including tray icons for quick changes.

This is a fork of [ideapad-perf](https://github.com/korikori/ideapad-perf) modified to fit my needs (using KDE Plasma on X11). The changes can in general be summed op to a rework of the ideapad-perf script (making it slightly easier to interact with for other scripts) and substituting the existing tray applications with a new one written in Python3 with Qt (using the PySide6 library). The original tray application scripts (which both used gtk) has been removed since they are not compatible with the modified script. Se the original authors repo if interested.

![screenshot](https://github.com/johandegn/ideapad-perf/blob/main/screenshot.png)

This rest of this readme has been changed to represent the changes represented in this fork.

## Motivation

The script is similar to [battmngr](https://github.com/0xless/battmngr), but the original script by korikori has been tested and confirmed to work on the following AMD models:
* IdeaPad 5 14ARE05 model 81YM. More information is available at the [ArchWiki](https://wiki.archlinux.org/title/Lenovo_IdeaPad_5_14are05#Power_management).
* IdeaPad 5 Pro 14ACN6 model 82L7. More information is available at the [ArchWiki](https://wiki.archlinux.org/title/Lenovo_IdeaPad_5_Pro_14ACN6#Power_management_options).

Since this script uses the exact same acpi calls as the original it should still work on the listed models (though i have only tested it on the 82L7 model).

You can check your own model by running
```sudo dmidecode -s system-product-name```.

**However, please have in mind that other Lenovo laptop models (especially Legion) have not been tested and are not expected to work with this script.**

## Requirements

The script requires the `acpi_call` module loaded for your kernel. The tray icon menu script requeres Python3 and the PySide6 library.

*More on ACPI modules on the [ArchWiki](https://wiki.archlinux.org/title/ACPI_modules).*

## Installation

You can download the script, make it executable, and add it to your path. You can run it with `sudo`, or you can install the supplied udev rule to make /proc/acpi/call writeable to all members of the `wheel` group.

If you wish to use the tray application i suggest that you make it autostart on login. There is usualy an option for this in most desktop environments. Remember to add the script to your path and make it executable for the tray application to work.

The applet icon used in the screenshot is `preferences-system-power.svg`, part of [Flatery Dark](https://github.com/cbrnix/Flatery).

## Usage

```
Usage: ideapad-perf OPTION

Options:
  -h,   --help                 Display this help text
  -v,   --version              Display version information
  -p,   --performance <mode>   Set performance mode
  -b,   --battery <mode>       Set battery mode
  -s,   --status               Print status for both performance and battery mode
  -sp,  --status-performance   Print status for performance mode
  -sb,  --status-battery       Print status for battery mode
  -spc, --sp-script            Print status for performance mode simplfied for scripting
  -sbc, --sb-script            Print status for battery mode simplfied for scripting

Performance modes:
  ic, intelligent              Intelligent Cooling
  ep, performance              Extreme Performance
  bs, battery                  Battery Saving

Battery modes:
  rc, rapid                    Enable Rapid Charge (with Battery Conservation disabled)
  bc, conserve                 Enable Battery Conservation (with Rapid Charge disabled)
  off                          Disable both Rapid Charge and Battery Conservation
```

## Note on Rapid Charge and Battery Conservation mode

It is possible to activate both Rapid Charge and Battery Conservation on Linux through the acpi calls. However, as this configuration is not obtainable using official Lenovo software on Windows and it would defeat the purpose of the Battery Conservation, it has been explicitly prevented in the script. Choosing one of the options will disable the other one first. If for any reason you need to achieve this effect, you can do so manually via the commands provided in the ArchWiki.

## Note on the system tray applets and Wayland

The script has not yet been tested on Wayland (only on X11). I suspect it to work, although i i cannot make any promises.

## License

This project is licensed under the GPL-3.0 License.
