def check_constraints(constraints, image_dim, window_axes):
    """Checks different window expansion constraints such as
    is it possible to expand from left or not and other too

    Parameters
    ----------
    constraints : tuple
        left, right, up, down window expansion constraints
    image_dim : tuple
        input image dimension (x, y) or (width, height)
    window_axes : tuple
        window axes (x1, x2, y1, y2) to check constraints

    Returns
    -------
    tuple
        Boolean values for constraints
    """
    # checks the movement of axes possible or not
    move_left, move_right, move_up, move_down = constraints
    x, y = image_dim
    x1, x2, y1, y2 = window_axes
    if x1<=0: move_left = False
    if x2>=x: move_right = False
    if y1<=0: move_up = False
    if y2>=y: move_down = False

    return (move_left, move_right, move_up, move_down)

#   ********************
#   *           ^    ^ *
#   *           y1   | *
#   *           |    | *
#   *        *****   | *
#   *        *   *  y2 *
#   *<--x1-->*   *   | *
#   *        *****   - *
#   *<---------x2----->*
#   *                  *
#   *                  *
#   ********************

def crop(image, center, aspect_ratio, expansion_value=5):
    """This function takes the image and crops it with desired aspect ratio

    Parameters
    ----------
    image : numpy array
        image array
    center : tuple
        h, k for center of window expansion
    aspect_ratio : float
        aspect ratio for window
    expansion_value : int, optional
        rate of window expansion, by default 5

    Returns
    -------
    numpy array
        cropped image array
    """
    h, k = center # center coordinates of face
    y, x = image.shape[:-1] # dimension of image

    dx = int(expansion_value) # expansion of window size from x-axis in pixel
    dy = int(dx/aspect_ratio) # expansion of window size from y-axis maintaining aspect aspect_ratio

    x1, x2, y1, y2 = h, h, k, k # placing center of expansion at center of image and moving outward

    move_left, move_right, move_up, move_down = True, True, True, True #

    while True:
        # expands window from every sides
        if not move_left and move_right and move_up and move_down:
            x1_ = x1-dx//2
            x2_ = x2+dx//2
            y1_ = y1-dy//2
            y2_ = y2+dy//2

        # expands windw from every sides except left or right
        elif not move_left or not move_right:
            if move_right:
                x1_ = x1
                x2_ = x2+dx

            if move_left:
                x1_ = x1-dx
                x2_ = x2

            if not move_up:
                y1_ = y1
                y2_ = y2+dy

            elif not move_down:
                y1_ = y1-dy
                y2_ = y2
            else:
                y1_ = y1-dy//2
                y2_ = y2+dy//2

        # expands windw from every sides except up or down
        elif (not move_up or not move_down) and move_left and move_right:
            x1_ = x1-dx//2
            x2_ = x2+dx//2
            if not move_up:
                y1_ = y1
                y2_ = y2+dy
            elif not move_down:
                y1_ = y1-dy
                y2_ = y2

        # checking the constraints after expansion
        move_left, move_right, move_up, move_down = check_constraints(
                (move_left, move_right, move_up, move_down),
                (x, y),
                (x1_, x2_, y1_, y2_)
            )

        # checking the terminating conditions
        if (not move_left and not move_right) or (not move_up and not move_down):
            break

        # checking the valid expansion and taking valid window
        if x1_>=0 and x2_<=x and y1_>=0 and y2_<=y:
            x1, x2, y1, y2 = x1_, x2_, y1_, y2_

    cropped_image = image[y1:y2, x1:x2, :] # cropping the window sized image

    return cropped_image