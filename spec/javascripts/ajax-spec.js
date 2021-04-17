beforeAll(function () {
    jasmine.Ajax.install()
})

describe("ajax operations", function () {
    describe("postColourChange", function () {
        it("posts a colour", function () {
            saveMode('direct')
            saveDirection('backwards')
            postColourChange([4, 5, 6])

            request = jasmine.Ajax.requests.mostRecent()

            expect(request.url).toBe('/desk/light')
            expect(request.method).toBe('POST')
            expect(request.contentType()).toEqual('application/json')
            expect(request.data()).toEqual({
                colour: [4, 5, 6],
                direction: 'backwards',
                mode: 'direct',
                delay: 0.01
            })
        })
    })

    describe("switchOff", function () {
        it("switches off", function () {
            colourPicker = jasmine.createSpyObj(['color'])

            setBG = jasmine.createSpy().and.callFake(setBG)
            colourButtons = jasmine.createSpy().and.callFake(colourButtons)

            switchOff()

            request = jasmine.Ajax.requests.mostRecent()

            expect(request.url).toBe('/desk/off')
            expect(request.method).toBe('POST')
            expect(request.contentType()).toEqual('application/json')

            expect(setBG).toHaveBeenCalledWith([0, 0, 0])
            expect(colourButtons).toHaveBeenCalledWith([0, 0, 0])
        })
    })
})
