from SimpleCV import Color, Image

def show_frame(display, parsed_frame, frame):
    if parsed_frame:
        bin_img = parsed_frame.center_img.binarize()
        parsed_frame.draw_frame(bin_img.dl())
        bin_img.save(display)
    else:
        frame.save(display)

def show_frame2(display, parsed_frame, frame):
    if parsed_frame:
        parsed_frame.bimg.save(display)
    else:
        frame.save(display)

def draw_grid(display, parsed_frame, frame):
    if parsed_frame:
        sl = parsed_frame.wall_states.shape[0]
        N = parsed_frame.wall_states.shape[1]

        chunk_w = 60
        chunk_h = 20

        img = Image((sl * chunk_w, N * chunk_h))
        dl = img.dl()

        for x in range(sl):
            for y in range(N):
                xp = x * chunk_w
                yp = (y+1)* chunk_h
                if parsed_frame.wall_states[x][N - y - 1]:
                    dl.rectangle((xp, yp), (chunk_w, chunk_h), color=Color.WHITE, filled=True)

        dl.circle((parsed_frame.cursor_angle * 2, chunk_h * N - 5), 5, color=Color.RED, filled=True)
        img.save(display)