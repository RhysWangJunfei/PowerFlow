filename = 'case30';
mpc = loadcase(filename);
%aa=runpf(mpc);
p_supply= csvread('p_supply2.csv');
vm_gen = csvread('vm_gen2.csv');
p_demand= csvread('p_demand2.csv');
q_demand= csvread('q_demand2.csv');
supply_mat_size = size(p_supply);
sample_size = supply_mat_size(1);
gen_number = supply_mat_size(2)-1;
bus_number = 30;
success_number = 0;
datapoints_list=[];
conditions_list=[];
for i=1:sample_size-1
    p_supply_i = p_supply(i+1,:);
    p_demand_i = p_demand(i+1,:);
    q_demand_i = q_demand(i+1,:);
    vm_gen_i = vm_gen(i+1,:);
    mpc.gen(:,2) = p_supply_i(2:gen_number+1)*100;
    mpc.gen(2:gen_number,6) = vm_gen_i(2:gen_number);
    mpc.bus(:,3) = p_demand_i(2:bus_number+1)*100;
    mpc.bus(:,4) = q_demand_i(2:bus_number+1)*100;
    [result,success]=runpf(mpc);
    if success==1 && all(result.gen(:,3)<result.gen(:,4)) && all(result.gen(:,3)>result.gen(:,5))
        success_number=success_number+1;
        datapoint = [result.bus(:,8).',result.bus(:,9).',result.gen(:,2).',result.gen(:,3).'];
        condition = [mpc.bus(:,3).',mpc.bus(:,4).'];
        datapoints_list = [datapoints_list;datapoint];
        conditions_list = [conditions_list;condition];
    end
end    
