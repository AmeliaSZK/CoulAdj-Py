
blue_12     = ( 10,  20, 230, 252)
green_10    = ( 10, 220,  30, 250)
cyan_8      = ( 10, 220, 230, 248)
red_6       = (210,  20,  30, 246)
magenta_4   = (210,  20, 230, 244)
yellow_2    = (210, 220,  30, 242)

blu = blue_12   
gre = green_10  
cya = cyan_8    
red = red_6     
mag = magenta_4 
yel = yellow_2  

cells = [
    [ [yel]*5, [mag]*3, [red]*1 ],
    [ [yel]*4, [cya]*1, [mag]*4 ],
    [ [gre]*2, [yel]*2, [cya]*4, [mag]*1 ],
    [ [gre]*2, [yel]*2, [cya]*4, [mag]*1 ],
    [ [gre]*4, [blu]*4, [mag]*1 ],
    [ [gre]*4, [blu]*4, [mag]*1 ],
    [ [gre]*4, [blu]*4, [mag]*1 ],
    [ [gre]*2, [red]*4, [blu]*2, [mag]*1 ]
]

print(cells)