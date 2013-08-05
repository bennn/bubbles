let assert_true e = 
  assert e

let assert_false e = 
  assert (not e)

let assert_greater v1 v2 =
  assert (v1 > v2)

let assert_less v1 v2 = 
  assert (v1 < v2)

let assert_equal v1 v2 = 
  assert (v1 = v2)
 
let assert_not_equal v1 v2 = 
  assert (v1 <> v2)

let assert_is v1 v2 =
  assert (v1 == v2)

let assert_is_not v1 v2 =
  assert (v1 != v2)
