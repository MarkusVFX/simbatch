gource --hash-seed 5  --date-format "refactoring in progress     %%Y-%%m-%%d %%H:%%M"  ^
--bloom-multiplier 1.5 --bloom-intensity 0.6 --caption-offset 40 --multi-sampling -e 0.4 ^
--font-size 22 --caption-duration 0.1 --caption-colour 7788FF --background 222531 --font-colour 88DDFF --filename-colour FFFFDD --dir-colour FFFFFF  ^
--frameless  --padding 1.3  --highlight-all-users --stop-at-end --logo-offset 0x0 --logo logo.png --filename-time 2.2  ^
--hide mouse -1280x720 --auto-skip-seconds 0.75 --seconds-per-day 0.13


REM -f   --title "www.SimBatch.com"    --title "refactoring in progress"

REM --output-ppm-stream c:\code-trunk.ppm

REM --hide progress
REM --date-format "%%%%D"

REM % gource --load-config  /path/to/multigource.conf -1280x720 {LOGFILE} --output-ppm-stream - | \
REM  ffmpeg -an -threads 4 -y -vb 4000000 -s 1280x720 -r 30 -f image2pipe -vcodec ppm -i - {OUTPUTFILE}
