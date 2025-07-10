from vehicle import Vehicle
from state import State, H, V


def make_map_01():
    ve1 = Vehicle((1 << 37) | (1 << 38), H)  #red car
    ve2 = Vehicle((1 << 54) | (1 << 46), V)
    ve3 = Vehicle((1 << 53) | (1 << 52) | (1 << 51), H)
    ve4 = Vehicle((1 << 50) | (1 << 49), H)
    ve5 = Vehicle((1 << 41) | (1 << 33), V)
    ve6 = Vehicle((1 << 35) | (1 << 27), V)
    ve7 = Vehicle((1 << 30) | (1 << 22) | (1 << 14), V)
    ve8 = Vehicle((1 << 13) | (1 << 12) | (1 << 11), H)
    ve9 = Vehicle((1 << 44) | (1 << 43), H)
    ve10 = Vehicle((1 << 26) | (1 << 25), H)
    ve11 = Vehicle((1 << 29) | (1 << 28), H)
    return [ve1, ve2, ve3, ve4, ve5, ve6, ve7, ve8, ve9, ve10, ve11]

def make_map_02():
    ve1 = Vehicle((1 << 37) | (1 << 36), H)  #red car
    ve2 = Vehicle((1 << 54) | (1 << 46), V)
    ve3 = Vehicle((1 << 53) | (1 << 52) | (1 << 51), H)
    ve4 = Vehicle((1 << 38) | (1 << 30) | (1 << 22), V)
    ve5 = Vehicle((1 << 14) | (1 << 13) | (1 << 12), H)
    ve6 = Vehicle((1 << 11) | (1 << 10), H)
    ve7 = Vehicle((1 << 21) | (1 << 20), H)
    ve8 = Vehicle((1 << 19) | (1 << 18), H)
    ve9 = Vehicle((1 << 28) | (1 << 27), H)
    ve10 = Vehicle((1 << 26) | (1 << 25), H)
    ve11 = Vehicle((1 << 43) | (1 << 35), V)
    ve12 = Vehicle((1 << 17) | (1 << 9), V)
    ve13 = Vehicle((1 << 42) | (1 << 41), H)
    return [ve1, ve2, ve3, ve4, ve5, ve6, ve7, ve8, ve9, ve10, ve11, ve12, ve13]

def make_map_03():
    ve1 = Vehicle((1 << 37) | (1 << 38), H)  #red car
    ve2 = Vehicle((1 << 53) | (1 << 52), H)
    ve3 = Vehicle((1 << 30) | (1 << 29) | (1 << 28), H)
    ve4 = Vehicle((1 << 21) | (1 << 20) | (1 << 19), H)
    ve5 = Vehicle((1 << 18) | (1 << 17), H)
    ve6 = Vehicle((1 << 10) | (1 << 9), H)
    ve7 = Vehicle((1 << 54) | (1 << 46), V)
    ve8 = Vehicle((1 << 44) | (1 << 36), V)
    ve9 = Vehicle((1 << 51) | (1 << 43), V)
    ve10 = Vehicle((1 << 49) | (1 << 41) | (1 << 33), V)
    ve11 = Vehicle((1 << 22) | (1 << 14), V)
    return [ve1, ve2, ve3, ve4, ve5, ve6, ve7, ve8, ve9, ve10, ve11]

def make_map_04():
    ve1 = Vehicle((1 << 37) | (1 << 38), H)  #red car
    ve2 = Vehicle((1 << 51) | (1 << 50) | (1 << 49), H)
    ve3 = Vehicle((1 << 45) | (1 << 44), H)
    ve4 = Vehicle((1 << 43) | (1 << 42) | (1 << 41), H)
    ve5 = Vehicle((1 << 30) | (1 << 29), H)
    ve6 = Vehicle((1 << 12) | (1 << 11), H)

    ve7 = Vehicle((1 << 54) | (1 << 46), V)
    ve8 = Vehicle((1 << 21) | (1 << 13), V)
    ve9 = Vehicle((1 << 36) | (1 << 28), V)
    ve10 = Vehicle((1 << 35) | (1 << 27), V)
    ve11 = Vehicle((1 << 26) | (1 << 18) | (1 << 10), V)
    ve12 = Vehicle((1 << 33) | (1 << 25), V)
    ve13 = Vehicle((1 << 17) | (1 << 9), V)
    return [ve1, ve2, ve3, ve4, ve5, ve6, ve7, ve8, ve9, ve10, ve11, ve12, ve13]

def make_map_05():
    ve1 = Vehicle((1 << 35) | (1 << 34), H)  #red car
    ve2 = Vehicle((1 << 53) | (1 << 52), H)
    ve3 = Vehicle((1 << 51) | (1 << 50), H)
    ve4 = Vehicle((1 << 18) | (1 << 17), H)
    ve5 = Vehicle((1 << 14) | (1 << 13), H)
    ve6 = Vehicle((1 << 11) | (1 << 10), H)
    ve7 = Vehicle((1 << 54) | (1 << 46), V)

    ve8 = Vehicle((1 << 38) | (1 << 30), V)
    ve9 = Vehicle((1 << 45) | (1 << 37) | (1 << 29), V)
    ve10 = Vehicle((1 << 44) | (1 << 36), V)
    ve11 = Vehicle((1 << 20) | (1 << 12), V)
    ve12 = Vehicle((1 << 27) | (1 << 19), V)
    ve13 = Vehicle((1 << 49) | (1 << 41) | (1 << 33), V)
    return [ve1, ve2, ve3, ve4, ve5, ve6, ve7, ve8, ve9, ve10, ve11, ve12, ve13]

def make_map_06():
    ve1 = Vehicle((1 << 37) | (1 << 36), H)  #red car
    ve2 = Vehicle((1 << 53) | (1 << 52) | (1 << 51), H)
    ve3 = Vehicle((1 << 42) | (1 << 41), H)
    ve4 = Vehicle((1 << 26) | (1 << 25), H)
    ve5 = Vehicle((1 << 20) | (1 << 19), H)
    ve6 = Vehicle((1 << 14) | (1 << 13), H)
    ve7 = Vehicle((1 << 12) | (1 << 11), H)

    ve8 = Vehicle((1 << 54) | (1 << 46) | (1 << 38), V)
    ve9 = Vehicle((1 << 30) | (1 << 22), V)
    ve10 = Vehicle((1 << 29) | (1 << 21), V)
    ve11 = Vehicle((1 << 43) | (1 << 35) | (1 << 27), V)
    ve12 = Vehicle((1 << 17) | (1 << 9), V)
    return [ve1, ve2, ve3, ve4, ve5, ve6, ve7, ve8, ve9, ve10, ve11, ve12]

def make_map_07():
    ve1 = Vehicle((1 << 35) | (1 << 36), H)  #red car
    ve2 = Vehicle((1 << 52) | (1 << 51), H)
    ve3 = Vehicle((1 << 50) | (1 << 49), H)
    ve4 = Vehicle((1 << 29) | (1 << 28), H)
    ve5 = Vehicle((1 << 18) | (1 << 17), H)
    ve6 = Vehicle((1 << 14) | (1 << 13), H)
    ve7 = Vehicle((1 << 12) | (1 << 11), H)

    ve8 = Vehicle((1 << 54) | (1 << 46), V)
    ve9 = Vehicle((1 << 38) | (1 << 30), V)
    ve10 = Vehicle((1 << 53) | (1 << 45) | (1 << 37), V)
    ve11 = Vehicle((1 << 27) | (1 << 19), V)
    ve12 = Vehicle((1 << 42) | (1 << 34) | (1 << 26), V)
    ve13 = Vehicle((1 << 33) | (1 << 25), V)
    return [ve1, ve2, ve3, ve4, ve5, ve6, ve7, ve8, ve9, ve10, ve11, ve12, ve13]

def make_map_08():
    ve1 = Vehicle((1 << 38) | (1 << 37), H)  #red car
    ve2 = Vehicle((1 << 49) | (1 << 50) | (1 << 51), H)
    ve3 = Vehicle((1 << 41) | (1 << 42), H)
    ve4 = Vehicle((1 << 29) | (1 << 28), H)
    ve5 = Vehicle((1 << 27) | (1 << 26), H)
    ve6 = Vehicle((1 << 21) | (1 << 20), H)
    ve7 = Vehicle((1 << 14) | (1 << 13), H)

    ve8 = Vehicle((1 << 30) | (1 << 22), V)
    ve9 = Vehicle((1 << 53) | (1 << 45), V)
    ve10 = Vehicle((1 << 52) | (1 << 44) | (1 << 36), V)
    ve11 = Vehicle((1 << 19) | (1 << 11), V)
    ve12 = Vehicle((1 << 33) | (1 << 25) | (1 << 17), V)
    return [ve1, ve2, ve3, ve4, ve5, ve6, ve7, ve8, ve9, ve10, ve11, ve12]

def make_map_09():
    ve1 = Vehicle((1 << 38) | (1 << 37), H)  #red car
    ve2 = Vehicle((1 << 53) | (1 << 52), H)
    ve3 = Vehicle((1 << 49) | (1 << 50) | (1 << 51), H)
    ve4 = Vehicle((1 << 44) | (1 << 43), H)
    ve5 = Vehicle((1 << 30) | (1 << 29), H)
    ve6 = Vehicle((1 << 27) | (1 << 26), H)
    ve7 = Vehicle((1 << 21) | (1 << 20), H)
    ve8 = Vehicle((1 << 14) | (1 << 13) | (1 << 12), H)

    ve9 = Vehicle((1 << 54) | (1 << 46), V)
    ve10 = Vehicle((1 << 36) | (1 << 28), V)
    ve11 = Vehicle((1 << 19) | (1 << 11), V)
    ve12 = Vehicle((1 << 42) | (1 << 34), V)
    ve13 = Vehicle((1 << 41) | (1 << 33) | (1 << 25), V)
    return [ve1, ve2, ve3, ve4, ve5, ve6, ve7, ve8, ve9, ve10, ve11, ve12, ve13]

def make_map_10():
    ve1 = Vehicle((1 << 35) | (1 << 34), H)  #red car
    ve2 = Vehicle((1 << 53) | (1 << 52), H)
    ve3 = Vehicle((1 << 30) | (1 << 29) | (1 << 28), H)
    ve4 = Vehicle((1 << 18) | (1 << 17), H)
    ve5 = Vehicle((1 << 13) | (1 << 14), H)
    ve6 = Vehicle((1 << 11) | (1 << 10), H)

    ve7 = Vehicle((1 << 54) | (1 << 46) | (1 << 38), V)
    ve8 = Vehicle((1 << 45) | (1 << 37), V)
    ve9 = Vehicle((1 << 44) | (1 << 36), V)
    ve10 = Vehicle((1 << 20) | (1 << 12), V)
    ve11 = Vehicle((1 << 27) | (1 << 19), V)
    ve12 = Vehicle((1 << 50) | (1 << 42), V)
    ve13 = Vehicle((1 << 41) | (1 << 33) | (1 << 25), V)
    return [ve1, ve2, ve3, ve4, ve5, ve6, ve7, ve8, ve9, ve10, ve11, ve12, ve13]