import KeyboardMouseDell as KM
import time
time.sleep(5)
for i in range(1, 5):
    KM.OpenSession("Experiment 1", i, "Mouse 123", 0)
    time.sleep(2)
    KM.IssueStart(i)
    time.sleep(5)
    KM.CloseSession(i)
    time.sleep(1)

for i in range(1, 5):
    KM.OpenSession("Experiment 1", i, "Mouse 123", 0)
    time.sleep(2)
    KM.IssueStart(i)
    time.sleep(5)
    KM.IssueKPulse(i)
    time.sleep(1)

for i in range(1,4):
    KM.OpenSession("Experiment 1", i, "Mouse 123", i-1)