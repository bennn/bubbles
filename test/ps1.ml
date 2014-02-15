let all_pairs (l : 'a list) : ('a * 'a) list =
  List.fold_left (fun acc x -> 
    List.fold_left (fun acc y -> 
      (x,y) :: acc) acc l) [] l

let fpe () = 
  1.0000001
