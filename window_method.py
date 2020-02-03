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
        if move_left is True and move_right is True and move_up is True and move_down is True:
            x1_ = x1-dx//2
            x2_ = x2+dx//2
            y1_ = y1-dy//2
            y2_ = y2+dy//2

        # expands windw from every sides except left or right
        elif move_left is False or move_right is False:
            if move_right is True:
                x1_ = x1
                x2_ = x2+dx

            if move_left is True:
                x1_ = x1-dx
                x2_ = x2

            if move_up is False:
                y1_ = y1
                y2_ = y2+dy

            elif move_down is False:
                y1_ = y1-dy
                y2_ = y2
            else:
                y1_ = y1-dy//2
                y2_ = y2+dy//2

        # expands windw from every sides except up or down
        elif (move_up is False or move_down is False) and move_left is True and move_right is True:
            x1_ = x1-dx//2
            x2_ = x2+dx//2
            if move_up is False:
                y1_ = y1
                y2_ = y2+dy
            elif move_down is False:
                y1_ = y1-dy
                y2_ = y2

        # checking the constraints after expansion
        move_left, move_right, move_up, move_down = check_constraints(
                (move_left, move_right, move_up, move_down),
                (x, y),
                (x1_, x2_, y1_, y2_)
            )

        # checking the terminating conditions
        if (move_left is False and move_right is False and move_up is False and move_down is True) or \
            (move_left is True and move_right is False and move_up is False and move_down is False) or \
                (move_left is False and move_right is False and move_up is True and move_down is False) or \
                    (move_left is False and move_right is True and move_up is False and move_down is False) or\
                        (move_left is False and move_right is False) or (move_up is False and move_down is False):
                        break

        # checking the valid expansion and taking valid window
        if x1_>=0 and x2_<=x and y1_>=0 and y2_<=y:
            x1, x2, y1, y2 = x1_, x2_, y1_, y2_

    cropped_image = image[y1:y2, x1:x2, :] # cropping the window sized image

    return cropped_image