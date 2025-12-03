def calculate_tatsp_cost(route, A , trigger_relations):
  
    total_cost = 0
    current_cost = A.copy()

    print("Rruga:" , route)
    print("---------------------")

    for i in range(len(route) - 1):
        arc = (route[i], route[i+1])
        cost = current_cost[arc]
        print(f"Arc: {arc} me kosto aktuale : {cost}")
    


    

  
