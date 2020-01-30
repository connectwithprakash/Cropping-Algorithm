def check_constraints(constraints, image_dim, window_axes):
    left, right, up, down = constraints
    x, y = image_dim
    x1, x2, y1, y2 = window_axes
    if x1<=0: left = False
    if x2>=x: right = False
    if y1<=0: up = False
    if y2>=y: down = False
        
    return (left, right, up, down)


def clip_image(image, center, output_dim, shift_value):
# x-axis adjustment
    h, k = center
    y, x = image.shape[:-1]
    a, b = output_dim
    ratio = a/float(b)
#     print(ratio)
    dx = int(shift_value)
    dy = int(dx/ratio)
#     print(dx, dy)
    x1, x2, y1, y2 = h, h, k, k

    left, right, up, down = True, True, True, True
    
    while True:
#         dx += int(shift_value)
#         dy = int(dx/ratio)
#         print(h, dx, k, dy)
        
        if left and right and up and down:
#             print('center')
            x1_ = x1-dx//2
            x2_ = x2+dx//2
            y1_ = y1-dy//2
            y2_ = y2+dy//2
            
            left, right, up, down = check_constraints(
                (left, right, up, down),
                (x, y),
                (x1_, x2_, y1_, y2_)
            )

        elif not left and right:
#             print('left end')
            x1_ = x1
            x2_ = x2+dx
#             print(f'up: {up}')
            if not up:
#                 print('left up end')
                y1_ = y1
                y2_ = y2+dy
#                 print(f'y2_ {y2_}')
            elif not down:
#                 print('left down end')
                y1_ = y1-dy
                y2_ = y2
            else:
#                 print('left end all open')
                y1_ = y1-dy//2
                y2_ = y2+dy//2
                
            left, right, up, down = check_constraints(
                (left, right, up, down),
                (x, y),
                (x1_, x2_, y1_, y2_)
            )
                
        elif not right and left:
#             print('right end')
            x1_ = x1-dx
            x2_ = x2
            if not up:
                y1_ = y1
                y2_ = y2+dy
            elif not down:
                y1_ = y1-dy
                y2_ = y2
            else:
                y1_ = y1-dy//2
                y2_ = y2+dy//2
                
            left, right, up, down = check_constraints(
                (left, right, up, down),
                (x, y),
                (x1_, x2_, y1_, y2_)
            )
        
        elif not up and down and left and right:
#             print('up end')
            x1_ = x1-dx//2
            x2_ = x2+dx//2
            y1_ = y1
            y2_ = y2+dy
            
            left, right, up, down = check_constraints(
                (left, right, up, down),
                (x, y),
                (x1_, x2_, y1_, y2_)
            )
                
        elif not down and up and left and right:
#             print('down end')
            x1_ = x1-dx//2
            x2_ = x2+dx//2
            y1_ = y1-dy
            y2_ = y2
            
            left, right, up, down = check_constraints(
                (left, right, up, down),
                (x, y),
                (x1_, x2_, y1_, y2_)
            )
#         print('********************************************************')
#         print(left, right, up, down)
                
        if (not left and not right and not up and down) or (left and not right and not up and not down) or\
        (not left and not right and up and not down) or (not left and not right and not up and down) or\
        (not left and not right) or (not up and not down):
#             print('break')
            break
        if x1_>=0 and x2_<=x and y1_>=0 and y2_<=y:
            x1, x2, y1, y2 = x1_, x2_, y1_, y2_
        
#         print(x1_, x2_, y1_, y2_)
#         print(x1, x2, y1, y2)
#         print(x2-x1, y2-y1)
            
            
#     print(image.shape)
#     print(image[y1:y2, x1:x2, :].shape)
    cropped_image = image[y1:y2, x1:x2, :]
    resized_image = cv2.resize(cropped_image, output_dim, interpolation=cv2.INTER_AREA)
    return resized_image