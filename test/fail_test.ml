open Ocamltest

let test_true_fail () =
  assert_true false

let test_false_fail () =
  assert_false true

let test_greater_fail () =
  assert_greater [] [1;2;3]

let test_less_fail () =
  assert_less 1000.0 1.0

let test_equal_fail () =
  assert_equal 9001 42

let test_not_equal_fail () =
  assert_not_equal (Some 'a') (Some 'a')

let test_is_fail () =
  assert_is "rolfcakes" "rolfcakes"

let test_is_not_fail () =
  let x = ref 11 in
  assert_is_not x x

let test_is_none_fail () =
  assert_is_none (Some None)

let test_is_not_none_fail () =
  assert_is_not_none None

let test_assert_raises_fail_noerr () =
  assert_raises (lazy (1/1)) Division_by_zero

let test_assert_raises_fail_err () =
  assert_raises (lazy (1/0)) Not_found
