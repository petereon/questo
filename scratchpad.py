from questo.select import Select, SelectState

select_state = SelectState(options=["a", "b", "a", "c"], title="Select a letter")

select = Select()

res = select.run(select_state)

print(res)
