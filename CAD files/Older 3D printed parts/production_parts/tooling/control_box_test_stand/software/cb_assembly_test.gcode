; This gcode is formulated for use with a Control Box Test Stand made for TAZ Workhorse Edition
; Use of this gcode outside of the testing process may result in damage or unexpected behavior
G21                          ; set units to millimetres
M107                         ; disable FAN 1
G90                          ; absolute positioning
M82                          ; set extruder to absolute mode
G92 E0                       ; set extruder position to 0
M400			     ; clear errors
M75			     ; start print timer

M117 Press X Min             ; display message
G28 X			     ; home X axis
G1 X150 F2500		     ; move to X max
M117 Press Y Min             ; display message
G28 Y			     ; home Y axis
G1 Y150 F2500		     ; move to Y min
M117 Press Z Max             ; display message
G28 Z			     ; home Z axis
G1 Z250 F500		     ; move to middle of Z axis
M400			     ; clear errors
M117 Press PROBE             ; display message
M226 P10 S1        	     ; wait for probe pin state change

G92 E0			     ; set E coordinate to zero
M117 E1 CCW                  ; display message
T0			     ; select T0
G0 E10 F100		     ; move T0 150mm
M400			     ; clear errors
M300 S440 P9		     ; play tone
M117 Press PROBE             ; display message
M226 P10 S1		     ; wait for probe pin state change
M117 E1 CW                   ; display message
G0 E0 F100		     ; retract T0 to 0 position 
M400			     ; clear errors
M300 S440 P9		     ; play tone
M117 Press PROBE             ; display message
M226 P10 S1		     ; wait for probe pin state change
M117 E2 CW                   ; display message
T1			     ; select T1
G0 E10 F100		     ; move T1 150mm
M400			     ; clear errors
M300 S440 P9		     ; play tone
M117 Press PROBE             ; display message
M226 P10 S1		     ; wait for probe pin state change
M117 E2 CCW                  ; display message
G0 E0 F100		     ; retract T1 to 0 position
M400			     ; clear errors
M300 S440 P9		     ; play tone
M117 Press PROBE             ; display message
M226 P10 S1		     ; wait for probe pin state change
T0			     ; select T0

M117 FAN 40 PERCENT          ; display message
M106 S102		     ; set cooling fan 0 to 40%

G4 S10			     ; dwell 3 seconds

M300 S440 P9		     ; play tone
M117 FAN 100 PERCENT         ; display message
M106 S255		     ; set cooling fan 0 to 100%

G4 S10			     ; dwell 3 seconds

M117 fan off                 ; display message
M107			     ; turn off cooling fan
M300 S440 P9		     ; play tone
M117 Heat 1                  ; display message
T0			     ; select T0
M104 S240		     ; set T0 temp to 240c
G4 S10			     ; wait
M104 S0			     ; turn T0 heat off
M300 S440 P9		     ; play tone
M117 Heat 2                  ; display message
T1			     ; select T1
M104 S240		     ; set T1 heat to 240c
G4 S10			     ; wait
M104 S0			     ; turn T1 heat off
M300 S440 P9		     ; play tone
M117 Bed Heat                ; display message
M140 S100		     ; set bed heat to 100c
G4 S10			     ; wait 
M140 S0			     ; turn bed heat off

M502			     ; restore factory defaults
M500			     ; save to EPROM
M77			     ; end print timer
M117 Test Complete           ; display message










