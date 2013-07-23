open First

let set_up () = 
  ()

let test_null () = 
  assert true

let test_add () = 
  assert (2 + 2 = 4)

let test_hd () =
  assert (First.hd [] = None)
