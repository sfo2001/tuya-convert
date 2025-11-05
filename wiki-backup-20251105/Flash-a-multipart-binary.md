!!!!! This method is deprecated for esp-HomeKit-devices as it already uses a combined binary, the method should be the same though for combining other binaries!!!

To flash a third party bin using `tuya-convert`, you will need to upload the firmware as a single binary.

Some projects might ask you to download and flash multiple files to different locations in flash. In that case, you will need to assemble the files into a single binary before flashing. Note that this is still subject to the 512KB limit for first upload.

As an example, we'll assemble a binary using the instructions from https://github.com/RavenSystem/esp-homekit-devices/wiki/Installation. It asks you to download and flash three separate binaries.

- [rboot.bin](https://github.com/SuperHouse/esp-open-rtos/raw/master/bootloader/firmware_prebuilt/rboot.bin), the bootloader, to be flashed at `0x0`
- [blank_config.bin](https://github.com/SuperHouse/esp-open-rtos/raw/master/bootloader/firmware_prebuilt/blank_config.bin), to be flashed at `0x1000`
- [haaboot.bin](https://github.com/RavenSystem/haa_ota/releases/latest/download/haaboot.bin), to be flashed at `0x2000`

We're going to use the utility `cat` to glue these files together, but before we do we must ensure that each part will end up in the right place in flash memory. So if we need to flash `blank_config.bin` at `0x1000`, `rboot.bin` must end at `0x1000`. To flash `haaboot.bin` at `0x2000`, we need `blank_config.bin` to end at `0x2000`, etc.

To pad `rboot` to `0x1000`, we can use `truncate`. Note that `0x1000` bytes is equal to `4KB`.

```bash
truncate -s 4k rboot.bin
```
Now we do the same for `blank_config`

```bash
truncate -s 4k blank_config.bin
```
We don't need to pad `haaboot` as there are no files after it. At this point we can safely concatenate the files together.
```bash
cat rboot.bin blank_config.bin haaboot.bin > thirdparty.bin
```
You can open `thirdparty.bin` in your hex editor of choice and verify that each segment is at the correct offset within the file.

Place `thirdparty.bin` in your `files` directory and you can now flash with the standard `tuya-convert` process.