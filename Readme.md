
# Retention Time Converter

## About RTC
Retention Time Converter is an open-source software for converting retention times in mzML data files. The goal of this python tool and application is to provide an easy-to-use utility for retention time conversions. With this tool you may convert the retention times within any mzML data to simulate if it was run under differing conditions, columns, or lengths of times. It is also useful for converting retention times to retention indices. This tool requires a reference file with the retention times of standard compounds run at the varying conditions.

## How to Use

A reference file in 'csv' format is required in order to convert retention times. For several examples see the included reference files 'RT6_TO_RTI.csv', and 'RT6_TO_RT27.csv'. The first file included converts the spectrums of a run over 6 minutes to a retention time indices using NAPS standards. The second included file converts the spectrums of a run over 6 minutes to the retention times over 27 minutes.

The standard format of these files is three columns with the first column containing the retention time or retention index of the standards in the type of run you would like to convert your file to. The second column includes the m/z of the the standard compound. The final column includes the retention times of the standard compounds run at the same conditions of your unconverted file.

Simply run the script at the command line or use the included .exe file to load up the tool. Keep in mind running the .exe file may take some time to load as it has to compile the code. It is included for those who wish to not use the command line. Simple browse to the locations of your reference file, your mzML, and the location/name of where you want to save your converted file. Click convert and wait until confirmation of conversion.
