function doSweep(colour, direction) {
    $.ajax({
        type: "POST",
        url: `/desk/all/sweep`,
        data: JSON.stringify(
            {
                'colour': colour,
                'direction': direction,
                'delay': 0.01
            }
        ),
        contentType: 'application/json',
    });
}

function hexToRGB(h) {
    let r = 0, g = 0, b = 0

    // 3 digits
    if (h.length == 4) {
        r = "0x" + h[1] + h[1]
        g = "0x" + h[2] + h[2]
        b = "0x" + h[3] + h[3]

        // 6 digits
    } else if (h.length == 7) {
        r = "0x" + h[1] + h[2]
        g = "0x" + h[3] + h[4]
        b = "0x" + h[5] + h[6]
    }

    return [+r, +g, +b]
}

function RGBToHex(rgb) {
    r = rgb[0].toString(16)
    g = rgb[1].toString(16)
    b = rgb[2].toString(16)

    if (r.length == 1)
        r = "0" + r
    if (g.length == 1)
        g = "0" + g
    if (b.length == 1)
        b = "0" + b

    return "#" + r + g + b
}
