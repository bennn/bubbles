open Assertions
open Ps1 

let test_all_pairs_null () = assert_equal [] (all_pairs [])

let test_all_pairs_single () = assert_equal [55,55] (all_pairs [55])

let test_all_pairs_triple () = assert_equal
  ([(1,1); (1,2); (1,3); (2,1); (2,2); (2,3); (3,1); (3,2); (3,3)])
  (List.sort compare (all_pairs [1;2;3]))
