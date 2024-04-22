import matplotlib.pyplot as plt

def Time_plot(x,a,b,c):
    # Draw time plot
    plt.plot(x, a, label='Min Conflict', color='b', linestyle='-', linewidth=2) 
    plt.plot(x, b, label='Total time Min Conflict', color='g', linestyle='--', linewidth=2) 
    plt.plot(x, c, label='Backtracking', color='r', linestyle='-.', linewidth=2) 

    # Add info
    plt.title("Tent puzzle time")
    plt.xlabel("Testcase")
    plt.ylabel("Time (ms)")
    plt.legend()
    plt.show()

def Mem_plot(x,a,b):
    # Draw memory plot
    plt.plot(x, a, label='Memory Min Conflict', color='g', linestyle='--', linewidth=2) 
    plt.plot(x, b, label='Memory Backtracking', color='r', linestyle='-.', linewidth=2) 

    # Add info
    plt.title("Tent puzzle memory")
    plt.xlabel("Testcase")
    plt.ylabel("Memory (byte)")
    plt.legend()
    plt.show()