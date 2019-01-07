# Card-Reader - PHP IC Reader

[C++ Version Download](https://forum.lowyat.net/index.php?s=484e91db040ef5380db8e751ef38c07e&act=Attach&type=post&id=255340) 
from lowyat forum user xenon

Python Version is in the Python folder

## Prerequisite
1. PHP Server
2. Smart Reader Device
3. PHP Extension (PSCS)

### Environment Setup
#### Smart Reader Devices
To connect the card reader to the system, it is required to install the appropriate driver.

Example 'ACR38U-N1' driver:

1. Download the installer from their site:
[https://www.acs.com.hk/download-driver-unified/9992/ACS-Unified-MSI-Win-4290.zip](https://www.acs.com.hk/download-driver-unified/9992/ACS-Unified-MSI-Win-4290.zip)
2. Unzip the file and
read the 'ReadMe' file and follow the instruction to install the device for usage.
3. After installation, the device can be used to read IC in PHP.

#### PHP Extension - Windows: PCSC
Assuming PHP server is setup and running...
1. Download the appropriate .dll from [https://pecl.php.net/package/pcsc/0.3.1/windows](https://pecl.php.net/package/pcsc/0.3.1/windows)

*to check the environment of the PHP, run "phpinfo()"*

2. Extract the .dll file to ..\php\ext
3. Edit php.ini by adding a new line "extension=php_pcsc.dll"
4. Restart server

#### PHP Server
On the off chance PHP server is not setup, XAMPP will be used.
1. Download XAMPP from [https://www.apachefriends.org/xampp-files/5.6.39/xampp-win32-5.6.39-0-VC11-installer.exe](https://www.apachefriends.org/xampp-files/5.6.39/xampp-win32-5.6.39-0-VC11-installer.exe)
2. Run the installer.
3. Run XAMMP control panel and start Apache and MySQL
4. Open web browser and enter "localhost"

*all runnable 'PHP' is located at "..\xampp\htdocs"*

Similarly, to install extension navigate to "..\xampp\php\ext" and add the appropriate .dll and edit 'php.ini' located at "..\xampp\php\"


#### PHP IC Scanner
1. Create a 'PCSC' folder at "..\xampp\htdocs" and an 'index.php' file.
2. Copy and paste the [code]() into the 'index.php'.
3. Start the server, plug in scanner, insert IC and open the web browser.
4. If everything is done correctly, it should display your basic IC information.


### Code Explanation

To access scanner device, windows pcsc api (installed for php) is used.
Similar syntax to "Winscard.h" (for C++), it is used in the same way.

There are 5 functions to remember:
1. scard_establish_context();
2. scard_list_readers(param);
3. scard_connect(param1, param2);
4. scard_transmit(param1, param2);
5. scard_release_context(param);

**Warning: There is no error checking**

#### scard_establish_context
This function initialise the use of IC reader. It will return a value which you will need to proceed.

Example:

      $context = scard_establish_context();

#### scard_list_readers(param)
Returns a list of available readers to be connected.

Example:

      $readers = scard_list_readers($context);

#### scard_connect(param1, param2)
Returns a value to allow communication to the specific device

Example:

      $connection = scard_connect($context, $readers[0]);

*caution: to access different readers, scroll through the values in "readers" and change the index*

#### scard_transmit(param1, param2)
Returns the response of the transmission in hexadecimal

Example:

      $res = scard_transmit($connection, $messageValue);

*Message transmitted should be in hexadecimal!*

Example:

      $messageValue = "CC060000"; // it is a string with hexadecimal format

#### scard_release_context(param)
It will close the reader appropriately

Example:

    scard_release_context($context);

### So what to send to the IC reader to get information?

A user in a forum "lowyat" called "xenon" posted a excellent [explanation](https://forum.lowyat.net/topic/355950/+20) to retrieve information from Malaysia IC, with [sample code and executible file](https://forum.lowyat.net/index.php?s=df29c677e79c6431cf8d22e1771847f1&act=Attach&type=post&id=255340).

The main idea to retrieve the information is by sending APDU commands (in Hexadecimal form).

To retrieve the information from Malaysia IC, there are 5 commands required (explained by user 'xenon'):
1. Select Application
2. Get Response
3. Set Length
4. Select Information
5. Read information

The basis of the command is based on TLV (Tag-Length-Value).

***
'Select Application' has 15 bytes of value:

index 0 to 9 (Default):

      0x00 0xA4 0x04 0x00 0x0A 0x0A0 0x00 0x00 0x00 0x74

index 10 to 12 (Select Option):

      Choose one of the following...
      1. JPN: 4A 50 4E
      2. JPJ: 4A 50 4A
      3. IMM: 49 4D 4D

      Based on which selection you wishes to retrieve information from.

index 13 to 14 (Default):

      0x00, 0x10

***
'Get Response' has 5 bytes of value:

Default:

      0x00 0xC0 0x00 0x00 0x05

The main purpose of this command is to check the previous command was successful. As such, when the response of 7 bytes returns, look for 90 00 at the end (index 5 and 6).

Example of Response:

      6F 03 82 01 38 90 00


***
'Set Length' has 10 bytes of value:

Index 0 to 7 (Default):

      0xC8 0x32 0x00 0x00 0x05 0x08 0x00 0x00

Index 8 to 9 (Value of length):
***
'Select Information' has 13 bytes of value:

index 0 to 4 (Default):

       0xCC 0x00 0x00 0x00 0x08

index 5 to 8 (Select Option):

      Choose only one:
      1. File 1: 0x01 0x00 0x01 0x00
      2. File 2: 0x02 0x00 0x01 0x00
      3. File 3: 0x03 0x00 0x01 0x00
      4. File 4: 0x04 0x00 0x01 0x00
      5. File 5: 0x05 0x00 0x01 0x00
      6. File 6: 0x06 0x00 0x01 0x00

      Caution!
      JPN has 6 files
      JPJ has 1 files
      IMM has 4 files

index 9 to 10 (Value of offset)
index of 11 to 12 (Value of length)
***
'Read Information' has 5 bytes:

index 0 to 3 (Default):

      0xCC 0x06 0x00 0x00

index 4 (Value of length)
***
#### Example of Retrieving Name from Malaysia IC

With any retrieval, they are located in a specific application, file and offset with a length. The information will be provided later but in this case to retrieve the name from the Malaysia IC, there are 3 location to retrieve from.

The table containing all retrieval information by 'xenon' shows that the 3 name information are:

- original name: jpn (application); 1 (file); 0003(offset); 96 (hex length)


- gmpc name: jpn (application); 1 (file); 0099(offset); 50 (hex length)


- kpt name: jpn (application); 1 (file); 00E9(offset); 28 (hex length)

Commands to retrieve original name...

Select Application:

      0x00, 0xA4, 0x04, 0x00, 0x0A, 0x0A0, 0x00, 0x00, 0x00, 0x74, 0x4A, 0x50, 0x4E, 0x00, 0x10

Get Response:

      0x00, 0xC0, 0x00, 0x00, 0x05

Set Length:

      0xC8, 0x32, 0x00, 0x00, 0x05, 0x08, 0x00, 0x00, 0x96, 0x00

Select Information:

      0xCC, 0x00, 0x00, 0x00, 0x08, 0x01, 0x00, 0x01, 0x00, 0x03, 0x00, 0x96, 0x00

Read Information:

      0xCC, 0x06, 0x00, 0x00, 0x96
***

### Offset and Length Table

The table are provided as images
