'''
Author: your name
Date: 2021-09-05 19:08:33
LastEditTime: 2021-09-07 07:40:10
LastEditors: Please set LastEditors
Description: 模拟mptcp两个流的throughput
FilePath: /Code/two-path-sim.py
'''
import os
import math
import matplotlib.pyplot as plt


# class flow:
#     def __init__(self, rtt, ssthresh, time) -> None:
#         """
#         init flow's rtt,cwnd
#         """
#         self.max_wnd = 80  # packets
#         self.cwnd = 1
#         self.rtt = rtt  # ms
#         if ssthresh is not None:
#             self.ssthresh = ssthresh
#         else:
#             self.ssthresh = self.max_wnd
#         self.sndwnd = self.cwnd
#         self.remain_time = time  # ms
#         self.mode = 1
#         # self.bw = bandwidth  # bps
#         pass

#     def update_sndwnd(self, distribution):
#         self.sndwnd = min(distribution, self.cwnd)

#     def update_rtt(self, dt):
#         """
#         mode means how to update rtt

#         1 for increasing 10ms everytime handover happens, 0 for decreasing
#         """
#         if self.mode == 1:
#             self.rtt += dt
#             if self.rtt >= 1000:
#                 self.mode = 0
#         else:
#             self.rtt -= dt
#             if self.rtt <= 10:
#                 self.mode = 1

#     def update_cwnd(self):
#         """
#         update flow's cwnd
#         mode: 1 for received ack, 0 for loss
#         """
#         if self.remain_time > 0:
#             if self.cwnd * 2 <= self.ssthresh:
#                 self.cwnd *= 2
#             else:
#                 self.cwnd += 1
#         # handover happens
#         elif self.remain_time <= 0 and self.remain_time > (-3*60*1000):
#             if self.cwnd != 0:
#                 self.ssthresh = self.cwnd // 2
#                 self.cwnd = 0
#                 self.update_rtt(10)
#         else:
#             self.cwnd = 1
#             self.remain_time = 3*60*1000


# if __name__ == '__main__':
#     # file_size = 1000  # MB
#     # packet_data_size = 1500-20-20  # Byte
#     # num_of_packets = file_size * 1000 * 1000 // packet_data_size
#     num_of_packets = 2000000
#     send_buffer_size = 100  # packets

#     subflow1 = flow(100, None, 3*60*1000)
#     subflow2 = flow(80, None, 2*60*1000)
#     subflow1.mode = subflow2.mode = 0

#     t = 0  # count time
#     throughput = []
#     time = []
#     while True:
#         # distribute packets to 2 subflows
#         distr1 = math.floor(send_buffer_size /
#                             (subflow1.rtt + subflow2.rtt) * subflow2.rtt)
#         distr2 = send_buffer_size - distr1
#         # print(distr1, distr2)
#         subflow1.update_sndwnd(distr1)
#         subflow2.update_sndwnd(distr2)
#         # print(subflow2.sndwnd, subflow1.sndwnd)
#         dt = max(subflow1.rtt, subflow2.rtt)
#         throughput.append((subflow1.sndwnd + subflow2.sndwnd)/dt*1000)
#         t += dt
#         subflow1.remain_time -= dt
#         subflow2.remain_time -= dt
#         subflow1.update_cwnd()
#         subflow2.update_cwnd()
#         subflow1.update_rtt(1)
#         subflow2.update_rtt(1)
#         time.append(t)
#         num_of_packets = num_of_packets - subflow1.sndwnd - subflow2.sndwnd
#         # break
#         # print(num_of_packets, "packets left")
#         if num_of_packets <= 0:
#             print("end time: ", t)
#             break
#         # if t > 10000:
#         #     break

#     num_of_packets = 2000000
#     send_buffer_size = 100  # packets

#     subflow1 = flow(100, None, 3*60*1000)
#     subflow2 = flow(80, None, 2*60*1000)
#     subflow1.mode = subflow2.mode = 1

#     t = 0  # count time
#     throughput2 = []
#     time2 = []
#     while True:
#         # distribute packets to 2 subflows
#         distr1 = math.floor(send_buffer_size /
#                             (subflow1.rtt + subflow2.rtt) * subflow2.rtt)
#         distr2 = send_buffer_size - distr1
#         # print(distr1, distr2)
#         subflow1.update_sndwnd(distr1)
#         subflow2.update_sndwnd(distr2)
#         # print(subflow2.sndwnd, subflow1.sndwnd)
#         dt = max(subflow1.rtt, subflow2.rtt)
#         throughput2.append((subflow1.sndwnd + subflow2.sndwnd)/dt*1000)
#         t += dt
#         subflow1.remain_time -= dt
#         subflow2.remain_time -= dt
#         subflow1.update_cwnd()
#         subflow2.update_cwnd()
#         subflow1.update_rtt(1)
#         subflow2.update_rtt(1)
#         time2.append(t)
#         num_of_packets = num_of_packets - subflow1.sndwnd - subflow2.sndwnd
#         # break
#         # print(num_of_packets, "packets left")
#         if num_of_packets <= 0:
#             print("end time: ", t)
#             break
#         # if t > 10000:
#         #     break

#     num_of_packets = 2000000
#     send_buffer_size = 100  # packets

#     subflow1 = flow(100, None, 3*60*1000)
#     subflow2 = flow(80, None, 2*60*1000)
#     subflow1.mode = 0

#     t = 0  # count time
#     throughput3 = []
#     time3 = []
#     while True:
#         # distribute packets to 2 subflows
#         distr1 = math.floor(send_buffer_size /
#                             (subflow1.rtt + subflow2.rtt) * subflow2.rtt)
#         distr2 = send_buffer_size - distr1
#         # print(distr1, distr2)
#         subflow1.update_sndwnd(distr1)
#         subflow2.update_sndwnd(distr2)
#         # print('sndwnd:', subflow2.sndwnd, subflow1.sndwnd)
#         # print('remain_time:', subflow2.remain_time, subflow1.remain_time)
#         # print('rtt:', subflow2.rtt, subflow1.rtt)
#         dt = max(subflow1.rtt, subflow2.rtt)
#         throughput3.append((subflow1.sndwnd + subflow2.sndwnd)/dt*1000)
#         t += dt
#         subflow1.remain_time -= dt
#         subflow2.remain_time -= dt
#         subflow1.update_cwnd()
#         subflow2.update_cwnd()
#         subflow1.update_rtt(1)
#         subflow2.update_rtt(1)
#         time3.append(t)
#         num_of_packets = num_of_packets - subflow1.sndwnd - subflow2.sndwnd
#         # break
#         # print(num_of_packets, "packets left")
#         if num_of_packets <= 0:
#             print("end time: ", t)
#             break
#         # if t > 10000:
#         #     break

#     num_of_packets = 2000000
#     send_buffer_size = 100  # packets

#     subflow1 = flow(100, None, 3*60*1000)
#     subflow2 = flow(80, None, 2*60*1000)
#     subflow1.mode = 0

#     t = 0  # count time
#     throughput4 = []
#     time4 = []
#     while True:
#         # distribute packets to 2 subflows
#         distr2 = math.floor(send_buffer_size / 2)
#         distr1 = send_buffer_size - distr2
#         # print(distr1, distr2)
#         subflow1.update_sndwnd(distr1)
#         subflow2.update_sndwnd(distr2)
#         # print('sndwnd:', subflow2.sndwnd, subflow1.sndwnd)
#         # print('remain_time:', subflow2.remain_time, subflow1.remain_time)
#         # print('rtt:', subflow2.rtt, subflow1.rtt)
#         dt = max(subflow1.rtt, subflow2.rtt)
#         throughput4.append((subflow1.sndwnd + subflow2.sndwnd)/dt*1000)
#         t += dt
#         subflow1.remain_time -= dt
#         subflow2.remain_time -= dt
#         subflow1.update_cwnd()
#         subflow2.update_cwnd()
#         subflow1.update_rtt(1)
#         subflow2.update_rtt(1)
#         time4.append(t)
#         num_of_packets = num_of_packets - subflow1.sndwnd - subflow2.sndwnd
#         # break
#         # print(num_of_packets, "packets left")
#         if num_of_packets <= 0:
#             print("end time: ", t)
#             break
#         # if t > 10000:
#         #     break

#     # print(throughput[:100])
#     # print(time[:100])
#     # print(throughput2[:100])
#     # print(time[:100])
#     # print(throughput3[:100])
#     # print(time[:100])
#     # print(throughput4[:100])
#     # print(time[:100])
#     l1, = plt.plot(time, throughput)
#     # l2, = plt.plot(time2, throughput2)
#     # l3, = plt.plot(time3, throughput3)
#     l4, = plt.plot(time4, throughput4)
#     plt.legend(handles=[l1, l4], labels=[
#                'rtt--_rrt_low_first', 'rtt--_rrt_robin'], loc='best')
#     # plt.plot(time[:1000], throughput[:1000])
#     # plt.plot(time2[:1000], throughput2[:1000])
#     # plt.plot(time3[:1000], throughput3[:1000])
#     # plt.plot(time4[:1000], throughput4[:1000])
#     plt.xlabel('time(ms)')
#     plt.ylabel('throughput(packet/s)')
#     plt.show()

#     pass
