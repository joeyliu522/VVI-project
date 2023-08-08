M73 P0                                    ; clear GLCD progress bar
M75			                  ; start GLCD timer
G21                                       ; set units to Millimetres
M107                                      ; disable fans
G90                                       ; absolute positioning
M420 S0                                   ; disable previous leveling matrix
T0                                        ; switch to nozzle 1
G28					  ; auto home
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
G1 X-49 Y-16 Z290 F9999			  ; move back up to top left 
G1 Z5 X285 Y308 F9999			  ; move to bottom right corner 
M106 S255				  ; fans a hundy P buddy

G1 Z5 F9999				  ; move up in Z a bit
G1 X-49 Y-16 F9999			  ; move to back left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z290 X285 Y308 F9999			  ; move to top right corner
G1 Z5 X-49 Y-16 F9999			  ; move to bottom left corner
G1 Z150 X285 Y308 F9999			  ; move to middle of Z axis

G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
G1 X-49 Y-16 F8500			  ; move only X/Y
G1 X285 Y308 F8500			  ; move only X/Y
M107					  ; fan off
G4 S1					  ; wait a tick
G28 Z					  ; home Z axis

M77					  ; end print timer

