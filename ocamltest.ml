exception Assert_true of string
let assert_true = function
| true -> ()
| false -> raise (Assert_true "false is not true")

exception Assert_false of string
let assert_false = function
| true -> raise (Assert_false "true is not false")
| false -> ()

exception Assert_greater of string
let assert_greater v1 v2 =
  match (v1 > v2) with
  | true -> ()
  | false -> 
    raise (Assert_greater (Printf.sprintf 
      "%s is not greater than %s" (Dump.truncate v1) (Dump.truncate v2)))

exception Assert_less of string
let assert_less v1 v2 = 
  match (v1 < v2) with
  | true -> ()
  | false -> 
    raise (Assert_less (Printf.sprintf 
      "%s is not less than %s" (Dump.truncate v1) (Dump.truncate v2)))

exception Assert_equal of string
let assert_equal v1 v2 = 
  match (v1 = v2) with
  | true -> ()
  | false -> 
    raise (Assert_equal (Printf.sprintf 
      "%s is not equal to %s" (Dump.truncate v1) (Dump.truncate v2)))

exception Assert_not_equal of string
let assert_not_equal v1 v2 = 
  match (v1 <> v2) with
  | true -> ()
  | false -> 
    raise (Assert_not_equal (Printf.sprintf 
      "%s is equal to %s" (Dump.truncate v1) (Dump.truncate v2)))

exception Assert_is of string
let assert_is v1 v2 =
  match (v1 == v2) with
  | true -> ()
  | false -> 
    raise (Assert_is (Printf.sprintf 
      "%s is not identical to %s" (Dump.truncate v1) (Dump.truncate v2)))

exception Assert_is_not of string
let assert_is_not v1 v2 =
  match (v1 != v2) with
  | true -> ()
  | false -> 
    raise (Assert_is_not (Printf.sprintf 
      "%s is the same as %s" (Dump.truncate v1) (Dump.truncate v2)))

exception Assert_is_none of string
let assert_is_none = function
| None -> ()
| Some x -> 
  raise (Assert_is_none (Printf.sprintf 
    "Some %s is not None" (Dump.truncate x)))

exception Assert_is_not_none of string
let assert_is_not_none = function
| None -> raise (Assert_is_not_none "expected Something, got None")
| Some _ -> ()

exception Assert_raises of string
let assert_raises expr ex : unit = 
  try 
    begin
      let _ = Lazy.force expr in raise (Assert_raises (Printf.sprintf
      "Forcing expression did not raise %s" (Printexc.to_string ex)))
    end 
  with 
    | Assert_raises _ as e -> raise e
    | e when e = ex -> ()
    | e -> raise (Assert_raises (Printf.sprintf 
      "Forcing the expression raised unexpected exception %s" (Printexc.to_string e)))
  
