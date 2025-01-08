import xlwings as xw
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

wb = xw.Book('shearwall_data_backup.xlsx')  # Replace with your file name
sheet = wb.sheets['SW_info']
ws = sheet 


last_row = sheet.range('D' + str(sheet.cells.last_cell.row)).end('up').row

# Retrieve the value from the last row of column D
last_row_value = int(sheet.range(f'D{last_row}').value)

print(f"Last Row Number: {last_row}")
print(f"Last Row Value: {last_row_value}")


# Calculate the starting row ID (D28 in this case)
start_row = last_row - last_row_value
start_cell_id = f'D{start_row}'
print(f"Start Cell ID: {start_cell_id}")


# Initialize a list to store wall dictionaries
walls = []
lengths = []
heights = []
x_list = []
y_list = []

# Run the for loop to extract data starting from D29 for `last_row_value` rows
for row in range(start_row + 1, start_row + 1 + last_row_value):
    wall = {
        'id': sheet.range(f'C{row}').value,
        'length': sheet.range(f'E{row}').value,
        'height': sheet.range(f'F{row}').value,
        'x': sheet.range(f'G{row}').value,
        'y': sheet.range(f'H{row}').value,
    }
    walls.append(wall)
    # Append individual attributes to their respective lists
    lengths.append(wall['length'])
    heights.append(wall['height'])
    x_list.append(wall['x'])
    y_list.append(wall['y'])


# Output the extracted walls data
# print("Extracted Walls Data:")
# Output the individual lists
# print(f"Lengths: {lengths}")
# print(f"Heights: {heights}")
# print(f"X Coordinates: {x_list}")
# print(f"Y Coordinates: {y_list}")

df_walls = pd.DataFrame(walls)
df_walls


# Get the last row in column P
last_row_ew = sheet.range('P' + str(sheet.cells.last_cell.row)).end('up').row

# Retrieve the number of walls from column P
num_walls_ew = int(sheet.range(f'P{last_row_ew}').value)


# Calculate the starting row ID for east-west walls
start_row_ew = last_row_ew - num_walls_ew
start_cell_id_ew = f'P{start_row_ew}'
print(f"Start Cell ID: {start_cell_id_ew}")


# Initialize lists for east-west direction walls
walls_ew = []
lengths_ew = []
heights_ew = []
x_list_ew = []
y_list_ew = []

# Run the for loop to extract data for east-west walls
for row in range(start_row_ew + 1, start_row_ew + 1 + num_walls_ew):
    wall_ew = {
        'id': sheet.range(f'O{row}').value,
        'length': sheet.range(f'Q{row}').value,
        'height': sheet.range(f'R{row}').value,
        'x': sheet.range(f'S{row}').value,
        'y': sheet.range(f'T{row}').value,
    }
    walls_ew.append(wall_ew)
    lengths_ew.append(wall_ew['length'])
    heights_ew.append(wall_ew['height'])
    x_list_ew.append(wall_ew['x'])
    y_list_ew.append(wall_ew['y'])


# (Assuming you have the north-south wall data in walls, x_list, y_list)
walls_combined = walls + walls_ew
x_combined = x_list + x_list_ew
y_combined = y_list + y_list_ew
lengths_combined = lengths + lengths_ew

df_walls_combined =  pd.DataFrame(walls_combined)
df_walls_combined

sheet.range('AC28').value = df_walls_combined

total_length_ns = sum(lengths)
com_x_ns = sum(length * x for length, x in zip(lengths, x_list)) / total_length_ns
# com_y_ns = sum(length * y for length, y in zip(lengths, y_list)) / total_length_ns


# # Output results to Excel
# sheet.range('J13').value = f"NS CoM: ({com_x_ns:.2f}, {com_y_ns:.2f})"
# sheet.range('J14').value = f"EW CoM: ({com_x_ew:.2f}, {com_y_ew:.2f})"

# Output results to Excel
sheet.range('J13').value = com_x_ns  # center of mass in x direction

# Calculate Center of Mass for East-West Walls
total_length_ew = sum(lengths_ew)
# com_x_ew = sum(length * x for length, x in zip(lengths_ew, x_list_ew)) / total_length_ew
com_y_ew = sum(length * y for length, y in zip(lengths_ew, y_list_ew)) / total_length_ew

# Output results to Excel
sheet.range('J14').value = com_y_ew  # center of mass in y direction

# Visualization using matplotlib
fig, ax = plt.subplots(figsize=(5, 4))  # Create figure and axis

# Plot north-south walls
for i, (x, y, length) in enumerate(zip(x_list, y_list, lengths)):
    ax.plot([x, x], [y, y + length], label=f"NS Wall {i+1}", color='blue')

# Plot east-west walls
for i, (x, y, length) in enumerate(zip(x_list_ew, y_list_ew, lengths_ew)):
    ax.plot([x, x + length], [y, y], label=f"EW Wall {i+1}", color='red')

# Add the (com_x_ns, com_y_ew) coordinate with a larger dot
ax.scatter(com_x_ns, com_y_ew, color='green', s=100, label='(CoM_x_NS, CoM_y_EW)', zorder=5)

# Formatting the plot
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_title('Shear Wall Layout')
# ax.legend(loc='upper right')
ax.grid(True)
ax.axis('equal')

# Embed the plot in Excel at cell O9
ws.pictures.add(fig, name='ShearWallPlot', update=True, anchor=ws.range("C64"))

# Display the plot (optional, for verification in Python)
plt.show()

#----------------------------------------------------------
# Initialize an empty list to store the normalized lengths
normalized_lengths_ew = []

# Loop through each length in the list
for length_ew in lengths_ew:
    # Divide the current length by the total length
    normalized_value_ew = length_ew / total_length_ew
    
    # Append the normalized value to the new list
    normalized_lengths_ew.append(normalized_value_ew)

# Print the result (optional)
print("Normalized Lengths for EW Walls:", normalized_lengths_ew)

# Output results to Excel
sheet.range('V29').options(transpose=True).value = normalized_lengths_ew


#----------------------------------------------------------
# Initialize an empty list to store the normalized lengths
normalized_lengths_ns = []

# Loop through each length in the list
for length in lengths:
    # Divide the current length by the total length
    normalized_value = length / total_length_ns
    
    # Append the normalized value to the new list
    normalized_lengths_ns.append(normalized_value)

# Print the result (optional)
print("Normalized Lengths for NS Walls:", normalized_lengths_ns)

# Output results to Excel
sheet.range('J29').options(transpose=True).value = normalized_lengths_ns

M_tor_ns = []
longest_dimension_ns = sheet.range('J10').value 
for length in lengths:
    M_tor_ns.append(0.1*longest_dimension_ns)

# Output results to Excel
sheet.range('K29').options(transpose=True).value = M_tor_ns


M_tor_ew = []
longest_dimension_ew = sheet.range('J11').value 
for length_ew in lengths_ew:
    M_tor_ew.append(0.1*longest_dimension_ew)

# Output results to Excel
sheet.range('W29').options(transpose=True).value = M_tor_ew


kdx_list = []
for idx,length_ns in enumerate(lengths):
    kdx_list.append(lengths[idx]*x_list[idx])
print(kdx_list)
kdx_list_sum = sum(kdx_list)

x_cr = kdx_list_sum/total_length_ns

print(x_cr)
# Output results to Excel
sheet.range('J16').value = x_cr

d_x_list = []
for idx,length_ns in enumerate(lengths):
    d_x_list.append(abs(x_cr-x_list[idx]))

print(d_x_list)
# Output results to Excel
sheet.range('I29').options(transpose=True).value = d_x_list


kdx_2_list = []
for idx,length_ns in enumerate(lengths):
    kdx_2_list.append(lengths[idx]*d_x_list[idx]**2)
    

print(kdx_2_list)

Jpx = sum(kdx_2_list)
print(Jpx)
# Output results to Excel
sheet.range('J19').value = Jpx

normalized_lengths_ns
V_total_ns_list = []
for idx,length_ns in enumerate(lengths):
    V_total_ns_list.append(normalized_lengths_ns[idx]+(M_tor_ns[idx]*kdx_list[idx])/Jpx)

print(V_total_ns_list)

# Output results to Excel
sheet.range('L29').options(transpose=True).value = V_total_ns_list


# Calculate kdy

kdy_list = []
for idx,length_ew in enumerate(lengths_ew):
    kdy_list.append(lengths_ew[idx]*y_list_ew[idx])

print(kdy_list)

kdy_list_sum = sum(kdy_list)

y_cr = kdy_list_sum/total_length_ew

print(y_cr)

# Output results to Excel
sheet.range('J17').value = y_cr

d_y_list = []
for idx,length_ew in enumerate(lengths_ew):
    d_y_list.append(abs(y_cr-y_list_ew[idx]))

print(d_y_list)

# Output results to Excel
sheet.range('U29').options(transpose=True).value = d_y_list

kdy_2_list = []
for idx,length_ew in enumerate(lengths_ew):
    kdy_2_list.append(lengths_ew[idx]*d_y_list[idx]**2)
    

print(kdy_2_list)

Jpy = sum(kdy_2_list)
print(Jpy)
# Output results to Excel
sheet.range('J20').value = Jpy


V_total_ew_list = []
for idx,length_ew in enumerate(lengths_ew):
    V_total_ew_list.append(normalized_lengths_ew[idx]+(M_tor_ew[idx]*kdy_list[idx])/Jpy)

print(V_total_ew_list)

# Output results to Excel
sheet.range('X29').options(transpose=True).value = V_total_ew_list