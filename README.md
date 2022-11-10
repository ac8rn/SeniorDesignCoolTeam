# SeniorDesignCoolTeam

hey gang, the comms files are not important, Zoe should have those, if you need them though, use the capitalized ones

also quick run down of how the code works:

1: ControlArray: each array is a circle or line that denotes a track the car is following, the code below shows what each number means
% circ/line(0/1), C_x/W1_x, C_y/W1_y, R/W2_x, CW/CCW (0,1) / W2_y,
    % Nx(halfplane), Ny(Halfplane), Px(halfplane), Py(Halfplane)
    
    1st pos: 1 or 0 denotes line or circle respectively
    2nd pos: denotes x coord of center for circ or x coord of first waypoint (start of line) for line
    3rd pos: denotes y coord of center for circ or y coord of first waypoint (start of line) for line
    4th pos: denotes radius length of circle or x coord of second waypoint (end of line) for line
    5th pos: denotes if the car is turning clockwise (0) or counter clockwise (1) for circ or y coord of second waypoint (end of line) for line
    6th pos: for both, denotes the x length of the normal vector to the halfplane (this is used to detect the change points to switch from array to array)
    7th pos: for both, denotes the y length of the normal vector to the halfplane
    8th pos: denotes the x coord of the intersection between the halfplane and current control line/circ
    9th pos: denotes the x coord of the intersection between the halfplane and current control line/circ
    
2: steerTable: each array is a series of angles measured by Zoe that characterize the actual angle behavior of the car servo configuration
    Zoe could honestly explain it better.
    
3: driveTable: same thing as above but with drive speeds

4: topLevel: function that runs the whole code in a while loop

5: intialize: function that sets the starting parameters of the car.
    X[0] is the x coord of the car initially
    X[1] is the y coord of the car initially
    X[2] is the angle of the car initally (180 is facing the negative x axis, 90, the pos y axis and etc.)
    U[0] is the control instruction to the drive motor (double check this)
    U[1] is the control instruction to the steer motor (double check this)
