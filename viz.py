def show_frame(display, parsed_frame, frame):
    if parsed_frame and parsed_frame.center_img:
        bin_img = parsed_frame.center_img.binarize()
        parsed_frame.draw_frame(bin_img.dl())
        bin_img.save(display)
    else:
        frame.save(display)