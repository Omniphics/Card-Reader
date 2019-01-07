<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="utf-8">
  <title></title>
</head>
<body>
  <?php

  # definition
  $CmdSelectAppJPN = "00A404000AA0000000744A504E0010";
  $CmdAppResponse = "00C0000005";
  $CmdSetLength = "C832000005080000";
  $CmdSelectFile = "CC00000008";
  $CmdGetData = "CC060000";
  $fileLengths = array(0, 458, 4011, 1227, 171, 43, 43, 0);

  # Get a PC/SC context
  $context = scard_establish_context();

  # Get the reader list
  $readers = scard_list_readers($context);

  # Use the first reader
  $reader = $readers[0];

  # Connect to the card
  $connection = scard_connect($context, $reader);

  # Select JPN
  $res = scard_transmit($connection, $CmdSelectAppJPN);
  $res = scard_transmit($connection, $CmdAppResponse);

  # Start Reading
  for ($FileNum = 1; $fileLengths[$FileNum]; $FileNum++) {
    for($split_offset = 0, $split_length =252; $split_offset < $fileLengths[$FileNum]; $split_offset += $split_length){
      if($split_offset + $split_length > $fileLengths[$FileNum]){
        $split_length = $fileLengths[$FileNum] - $split_offset;
      }

      # Select the reading length
      $setLength = $CmdSetLength.sprintf("%02X", $split_length)."00";
      $selectFile = $CmdSelectFile.sprintf("%02X", $FileNum)."000100".sprintf("%02X", $split_offset)."00".sprintf("%02X", $split_length)."00";
      $getData = $CmdGetData.sprintf("%02X", $split_length);

      # Asking for response
      $res = scard_transmit($connection, $setLength);
      $res = scard_transmit($connection, $selectFile);
      $res = scard_transmit($connection, $getData);

      if ($FileNum == 1 && $split_offset == 0) {
        $text = hex2bin(substr($res, 2*3, 2*40));
        echo "Name: ".$text."<br>";

			}
      elseif($FileNum == 1 && $split_offset ==252){
        $text = hex2bin(substr($res, 2*273 - 2*252, 2*13));
        echo "IC: ".$text."<br>";

        $text = hex2bin(substr($res, 2*286 - 2*252, 2*1));
        if($text == "L")
        {
          echo "Sex: Male<br>";
        }
        elseif($text == "P"){
          echo "Sex: Female<br>";
        }

        $text = hex2bin(substr($res, 2*287 - 2*252, 2*8));
        echo "Old IC: ".$text."<br>";

        $text = hex2bin(substr($res, 2*295 - 2*252, 2*4));
        echo "DOB: ".substr($res, 2*295 - 2*252, 2*4)."<br>";

        $text = hex2bin(substr($res, 2*299 - 2*252, 2*25));
        echo "State of Birth: ".$text."<br>";

        $text = hex2bin(substr($res, 2*324 - 2*252, 2*4));
        echo "Validity Date: ".substr($res, 2*324 - 2*252, 2*4)."<br>";

        $text = hex2bin(substr($res, 2*328 - 2*252, 2*18));
        echo "Nationality: ".$text."<br>";

        $text = hex2bin(substr($res, 2*346 - 2*252, 2*25));
        echo "Ethnic/Race: ".$text."<br>";

        $text = hex2bin(substr($res, 2*371 - 2*252, 2*11));
        echo "Religion: ".$text."<br>";
      }
      if ($FileNum == 4 && $split_offset == 0) {
        $text = hex2bin(substr($res, 2*3, 2*30));
        echo "<br>Address:<br>".$text."<br>";
        $text = hex2bin(substr($res, 2*33, 2*30));
        echo $text."<br>";
        $text = hex2bin(substr($res, 2*63, 2*30));
        echo $text."<br>";
        $text = hex2bin(substr($res, 2*93, 2*3));
        echo substr($res, 2*93, 2*3)."<br>";
        $text = hex2bin(substr($res, 2*96, 2*25));
        echo $text."<br>";
        $text = hex2bin(substr($res, 2*121, 2*30));
        echo $text."<br>";
      }

    }
  }

  # Release the PC/SC context
  scard_release_context($context);


  ?>
</body>
</html>
