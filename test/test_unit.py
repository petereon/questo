from questo import hello
from ward import test
from expycted import expect

for name in ["Jozo", "Fero", "Jano"]:
    @test(f'"Hello, {name}" gets printed')
    def _(name_in=name):
        expect(hello(name_in)).to.be_equal_to(f'Hello, {name_in}')
