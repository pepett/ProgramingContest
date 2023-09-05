@staticmethod
def n_dup(arr,is_rough):
	v_arr=arr
	result=[]
	n=[]
	while True:#v_arrがなくなるまでループ
		v_arr_first=v_arr.pop(0)#カウントする要素を取得
		v_arr_update=[]#タグを取り除いた配列
		j=1#タグの個数
		for i in v_arr:
			if i==v_arr_first:#v_arr_firstと元の配列がかぶっているか
				j+=1#かぶっていたら+1(タグの個数を記録)
				continue#かぶっていたら追加しない
			v_arr_update.append( i )#まだ重複チェックしてないものを残す
		n.append(j)
		result.append(v_arr_first)
		v_arr.clear()
		v_arr.extend( v_arr_update )
		if len(v_arr)==0:
			break
	return ( result, n )
data,eval = n_dup( [ 'true','false','true','elif','false','true','elif','elif','else','if' ], True )
print( eval )