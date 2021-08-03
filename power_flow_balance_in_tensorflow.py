x_input=np.array([0,2.566,1.386,0,1.102,0.452]).reshape([-1,6])
g_p = tf.convert_to_tensor(np.array([4.095,0,0]))
gs_q = tf.convert_to_tensor(np.array([1.89,0,0]))
vm = tf.convert_to_tensor(np.array([1.05,0.98183,1.00125]))
va=tf.convert_to_tensor(np.array([0,-3.5035,-2.8624]))
p_bus = np.zeros([batch_size,3])
q_bus = np.zeros([batch_size,3])
for j in range(0,3):
  p_bus[:,j] = x_input[:,j*2]
  q_bus[:,j] = x_input[:,j*2+1]
p_bus_tf = tf.convert_to_tensor(p_bus)
q_bus_tf = tf.convert_to_tensor(q_bus)
p_bus_tf = p_bus_tf-g_p
q_bus_tf = q_bus_tf-gs_q
#Get Y_bus
Y_bus_tf = tf.convert_to_tensor(Y_bus)

v_r = tf.math.multiply(vm,tf.cos(tf.math.multiply(va,tf.constant(math.pi/180,dtype='float64'))))
v_i = tf.math.multiply(vm,tf.sin(tf.math.multiply(va,tf.constant(math.pi/180,dtype='float64'))))
V = tf.reshape(tf.complex(v_r,v_i),[3,1])
vj_vi = V-tf.transpose(V)
y_vj_vi = tf.math.multiply(Y_bus_tf,vj_vi)
v_expand = tf.repeat(V,3,axis=1)
s_ij = tf.math.multiply(v_expand,tf.math.conj(y_vj_vi))
S_in = tf.reshape(tf.reduce_sum(s_ij,axis=1),[3,1])
I = tf.matmul(Y_bus_tf,V)
S_out = tf.math.multiply(V,tf.math.conj(I))
#print(S_out)
ss=S_in+S_out
print(abs(ss.numpy())<0.001)
