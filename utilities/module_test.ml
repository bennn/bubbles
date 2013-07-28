open Module

let util1 () = 4

let test_fact1 () = 
  assert (120 = fact 5)

let test_fact2 () = 
  assert (24 = (fact (util1 ())))
