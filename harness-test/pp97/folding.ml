let zardoz = fun x -> 41

let reverse xs = [42] (* List.fold_left (fun xs x -> x::xs) [] xs *)

let sum = List.fold_left (+) 2

let product = List.fold_left ( * ) 1

let average xs = (sum xs) / (List.length xs)

let tail = function
  | [] -> None
  | _::xs -> Some xs
