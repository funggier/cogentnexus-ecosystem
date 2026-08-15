# คู่มือติดตั้ง CogentNexus Ecosystem v0.2.0 แบบจับมือทำ

คู่มือนี้ใช้ **หลังจากติดตั้ง CogentNexus Core v0.8.x สำเร็จแล้ว** และต้องการเพิ่ม `staged-capability-loop` เพื่อให้การเลือก DIRECT / LOOKUP / ACTION / STAGED มี policy/review contract ที่ชัดเจนขึ้น

## 1. ตรวจ Core ก่อน

เปิด PowerShell:

```powershell
Set-Location "$HOME\.openclaw\workspace"
.\cnx.cmd status
```

ควรเห็น Host อยู่ MANAGED และ Gateway healthy

ตรวจไฟล์ Core baseline:

```powershell
Test-Path ".\skills\cogentnexus\scripts\host.py"
Test-Path ".\skills\cogentnexus\templates\AGENTS.cogentnexus.md"
```

ทั้งสองคำสั่งควรได้ `True`

ถ้าไม่ใช่ ให้ติดตั้ง/อัปเดต Core ก่อน

## 2. ดาวน์โหลด Ecosystem release

```powershell
Set-Location "$HOME\Downloads"
New-Item -ItemType Directory -Force ".\CogentNexus-Ecosystem" | Out-Null
Set-Location ".\CogentNexus-Ecosystem"

$version = "v0.2.0"
$base = "https://github.com/funggier/cogentnexus-ecosystem/releases/download/$version"
Invoke-WebRequest "$base/cogentnexus-ecosystem-$version.zip" -OutFile "cogentnexus-ecosystem-$version.zip"
Invoke-WebRequest "$base/SHA256SUMS.txt" -OutFile "SHA256SUMS.txt"
```

## 3. ตรวจ SHA256

```powershell
$actual = (Get-FileHash ".\cogentnexus-ecosystem-v0.2.0.zip" -Algorithm SHA256).Hash.ToLower()
$expected = ((Get-Content ".\SHA256SUMS.txt" | Select-String "cogentnexus-ecosystem-v0.2.0.zip") -split "\s+")[0].ToLower()
if ($actual -ne $expected) { throw "SHA256 mismatch - ห้ามติดตั้ง" }
Write-Host "SHA256 OK"
```

ต้องเห็น `SHA256 OK`

## 4. แตกไฟล์

```powershell
Expand-Archive ".\cogentnexus-ecosystem-v0.2.0.zip" -DestinationPath ".\cogentnexus-ecosystem-v0.2.0" -Force
Set-Location ".\cogentnexus-ecosystem-v0.2.0\cogentnexus-ecosystem-v0.2.0"
```

ตรวจ:

```powershell
Test-Path ".\scripts\install.py"
```

ต้องได้ `True`

## 5. ติดตั้งเข้า workspace เดียวกับ Core

```powershell
python .\scripts\install.py --workspace "$HOME\.openclaw\workspace"
```

Installer จะ:

1. ตรวจว่า Core Host baseline มีอยู่จริง
2. backup `staged-capability-loop` เดิมถ้ามี
3. copy skill ใหม่
4. validate ไฟล์หลัก
5. backup `AGENTS.md`
6. แทนเฉพาะ block ระหว่าง `<!-- cogentnexus:begin -->` และ `<!-- cogentnexus:end -->`
7. ไม่แตะ policy ของคุณที่อยู่นอก managed block

เมื่อสำเร็จจะบอกให้เริ่ม OpenClaw session ใหม่

## 6. ตรวจไฟล์หลังติดตั้ง

```powershell
Set-Location "$HOME\.openclaw\workspace"
Test-Path ".\skills\staged-capability-loop\SKILL.md"
```

ต้องได้ `True`

ตรวจ managed block:

```powershell
Get-Content ".\AGENTS.md"
```

ควรเห็นหัวข้อ:

```text
CogentNexus Ecosystem - Managed Continuity and Routing
```

และควรมีลำดับที่ **เลือก lane ก่อนโหลด `cogentnexus` heavy machinery**

## 7. restart Gateway / เปิด session ใหม่

เพื่อให้ workspace instructions/skill metadata reload ชัดเจน:

```powershell
.\cnx.cmd restart
```

จากนั้นเปิด session ใหม่ใน OpenClaw

## 8. ทดสอบ DIRECT

ส่ง:

```text
สวัสดีครับ
```

สิ่งที่ต้องการ:

```text
Ticket-first continuity
 -> DIRECT
 -> ตอบธรรมดา
```

ไม่ควรมี workflow announcement, contract, checkpoint หรือ reviewer เพียงเพราะเป็น CogentNexus

## 9. ทดสอบ STAGED

ส่งงานหลายขั้นที่ชัดเจน เช่นงานสร้าง artifact พร้อม validation หลายข้อ

สิ่งที่ต้องการคือระบบสามารถเลือก STAGED เมื่อ complexity/risk เหมาะสม และใช้ durable workflow/verification เฉพาะตรงนั้น

## 10. ทดสอบ PASSTHROUGH

```powershell
.\cnx.cmd disable
```

หลัง disable OpenClaw ต้องยังใช้งานได้ตามปกติ และ CogentNexus managed policy จะถูกเอาออกโดย Core Host

เปิดกลับ:

```powershell
.\cnx.cmd enable
```

จากนั้นรัน ecosystem installer ซ้ำถ้าต้องการให้ combined ecosystem policy กลับมาแทน Core-only policy block แล้ว restart/open fresh session อีกครั้ง

> หมายเหตุ: `cnx enable` คืน Core managed policy; ecosystem installer เป็นเจ้าของ combined policy ดังนั้นหลัง PASSTHROUGH -> enable ให้ reinstall ecosystem companion เพื่อคืน combined routing policy เวอร์ชันที่ต้องการ

## Checklist

```text
[ ] Core v0.8.x ติดตั้งแล้ว
[ ] cnx status = managed
[ ] ecosystem SHA256 ผ่าน
[ ] install.py สำเร็จ
[ ] staged-capability-loop มีอยู่
[ ] AGENTS managed block เป็น Ecosystem policy
[ ] greeting ใช้ DIRECT
[ ] complex task สามารถใช้ STAGED
[ ] cnx disable แล้ว OpenClaw native ใช้ได้
```
