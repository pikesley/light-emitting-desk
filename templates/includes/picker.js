var colourPicker = new iro.ColorPicker("#colour-picker", {
    width: 600,
    color: "rgb(255, 255, 255)",
    layout: [
        {
            component: iro.ui.Wheel,
        },
        // {
        //     component: iro.ui.Slider,
        // },
    ]
})

colourPicker.on('input:end', function (colour) {
    setColour(colour)
})

colourPicker.on('mount', function (picker) {
    $.get("/desk/all", function (data) {
        colour = data.colour
        if (isBlack(colour)) {
            colour = [255, 255, 255]
        }
        picker.color.rgb = {
            r: colour[0],
            g: colour[1],
            b: colour[2]
        }
    });
})
