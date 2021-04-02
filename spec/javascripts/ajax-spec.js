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
})
