
# coding: utf-8

# # Bin Packing Optimization for AWS EC2 Instances

# This notebook shows a way to optimize AWS EC2 usage using bin packing optimization.<br>
# I used [Openopt](https://pypi.python.org/pypi/openopt) to make a model and solve the program.<br>
# To install openopt, run the following command.
# 
# ```
# conda install --channel https://conda.anaconda.org/cachemeorg funcdesigner openopt
# pip install cvxopt
# pip install glpk
# ```
# 
# This program is for python3.5 with Anaconda.
# <br><br>
# ### Problem to solve:
# Assume you have several applications to run on public cloud(say, AWS EC2), for 24/7.<br>
# You know the number of applications and how much resources each application uses.<br>
# Your objective is to install and run the applications to EC2 instances with cost optimized.<br>
# What it means by cost optimized is that you have to make the cost less as possible.<br>
# Which instance sizes and how many instances do you choose to run the applications?

# In[1]:

# import openopt
from openopt import *


# In[6]:

# number of each application by size
small_num = 20
med_num = 12
large_num = 9

apps = []

# make a list of dictionary of the applications
for i in range(small_num):
    small_app = {
        'name': 'small%d' % i,
        'cpu': 0.2,
        'mem': 256,
        'disk': 1
        }
    apps.append(small_app)

for i in range(med_num):
    med_app = {
        'name': 'medium%d' % i,
        'cpu': 0.5,
        'mem': 512,
        'disk': 10
        }
    apps.append(med_app)
    
for i in range(large_num):
    large_app = {
        'name': 'large%d' % i,
        'cpu': 2.4,
        'mem': 2048,
        'disk': 40
        }
    apps.append(large_app)


# In[3]:

# instance size to choose from

instance_sizes = [
    {
        'name': 'm4.x4large',
        'cost': 1.032 * 24 * 30,
        'size': {
            'cpu': 16,
            'mem': 64 * 1024, 
            'disk': 1000
        }
    },
    {
        'name': 'r3.2xlarge',
        'cost': 0.798 * 24 * 30,
        'size': {
            'cpu': 8,
            'mem': 61 * 1024, 
            'disk': 1000
        }
    },
    {
        'name': 'c4.2xlarge',
        'cost': 0.504 * 24 * 30,
        'size': {   
            'cpu': 8,
            'mem': 15 * 1024, 
            'disk': 1000 
        }
    }
]


# In[4]:

# bin packing
# returns solved model, number of instances to use and the total cost
def bin_pack_instance(apps, instance_size):
    cost = instance_size['cost']    
    p = BPP(apps, instance_size['size'], goal = 'min')
    r = p.solve('glpk', iprint = 0)
    instances = len(r.xf)
    total_cost = instances * cost
    return r, instances, total_cost


# In[22]:

if __name__ == '__main__':
    for instance in instance_sizes:
        r, instances, total_cost = bin_pack_instance(apps, instance)

        print("\r") 
        print("Bin packing for : {0}".format(instance['name']))
        print("Total number of apps is " + str(len(apps)))
        print("Total {0} instance used is {1}".format(instance['name'], instances))
        print("Total cost is {0}".format(total_cost))

        for i,s in enumerate(r.xf):
            print ("Instance {0} contains {1} apps".format(i, len(s)))
            print("\t CPU: {0}vCPU\t RAM: {1}MB\t Disk: {2}GB"
                  .format(r.values['cpu'][i], r.values['mem'][i], r.values['disk'][i]))
            print("\t Contains: {0}".format(r.xf[i]))

        print("\r")  


# ### Result
# Now you know from the total cost of the instances, it is efficient to use 4 c4.2xlarge instances for the applications.

# In[ ]:



