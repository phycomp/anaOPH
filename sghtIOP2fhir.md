視力 IOP 轉成 fhir bundle

要將視力和眼內壓（IOP）數據轉換為 FHIR 格式的 Bundle，需要創建多個 FHIR 資源，然後將它們組合在一起，形成一個 FHIR Bundle 資源。視力和眼內壓數據屬於臨床觀察，因此可以用 FHIR 的 Observation 資源來表示。最後，將這些 Observation 資源放入 FHIR 的 Bundle 中進行傳輸。

實現步驟
創建 FHIR Patient 資源：首先，定義與視力和眼內壓相關的患者。
創建 FHIR Observation 資源：將視力和眼內壓值轉換為 Observation 資源，並且每個 Observation 資源都應包括與該觀察值相關的信息，例如日期、數值和單位等。
創建 FHIR Bundle 資源：將這些資源組合為一個 Bundle 資源，以便一次性傳輸所有相關數據。
1. 創建 Patient 資源 這個資源表示接受檢查的患者。

from fhir.resources.patient import Patient

# 創建患者資源
patient = Patient( id="123", name=[{"family": "Smith", "given": ["John"]}], gender="male", birthDate="1980-01-01")
2. 創建 Observation 資源
接下來，為視力和眼內壓創建觀察資源。視力和 IOP 通常以兩個獨立的 Observation 資源來表示。

視力（Visual Acuity）Observation
from fhir.resources.observation import Observation
from fhir.resources.coding import Coding

# 視力觀察
visual_acuity_observation = Observation( id="obs1", status="final",
    code={"coding": [{"system": "http://loinc.org", "code": "29544-3", "display": "Visual acuity"}]},
    subject={"reference": f"Patient/{patient.id}"},
    effectiveDateTime="2024-09-12T12:00:00Z",  # 測量日期
    valueQuantity={"value": 0.8, "unit": "1", "system": "http://unitsofmeasure.org", "code": "1"}
)
眼內壓（IOP）Observation
# 眼內壓觀察
iop_observation = Observation( id="obs2", status="final",
    code={"coding": [{"system": "http://loinc.org", "code": "17864-0", "display": "Intraocular pressure"}]},
    subject={"reference": f"Patient/{patient.id}"},
    effectiveDateTime="2024-09-12T12:00:00Z",  # 測量日期
    valueQuantity={"value": 18, "unit": "mmHg", "system": "http://unitsofmeasure.org", "code": "mm[Hg]"}
)
3. 創建 Bundle 資源
將這些資源組合成一個 Bundle，它包含 Patient 和 Observation 資源。

from fhir.resources.bundle import Bundle, BundleEntry

# 創建 Bundle
bundle = Bundle(
    type="collection",
    entry=[
        BundleEntry(resource=patient),
        BundleEntry(resource=visual_acuity_observation),
        BundleEntry(resource=iop_observation)
    ]
)

# 輸出 Bundle 資源為 JSON
pprint(bundle.json(indent=2))
{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    {
      "resource": {
        "resourceType": "Patient",
        "id": "123",
        "name": [
          {
            "family": "Smith",
            "given": ["John"]
          }
        ],
        "gender": "male",
        "birthDate": "1980-01-01"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "id": "obs1",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "29544-3",
              "display": "Visual acuity"
            }
          ]
        },
        "subject": {
          "reference": "Patient/123"
        },
        "effectiveDateTime": "2024-09-12T12:00:00Z",
        "valueQuantity": {
          "value": 0.8,
          "unit": "1",
          "system": "http://unitsofmeasure.org",
          "code": "1"
        }
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "id": "obs2",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "17864-0",
              "display": "Intraocular pressure"
            }
          ]
        },
        "subject": {
          "reference": "Patient/123"
        },
        "effectiveDateTime": "2024-09-12T12:00:00Z",
        "valueQuantity": {
          "value": 18,
          "unit": "mmHg",
          "system": "http://unitsofmeasure.org",
          "code": "mm[Hg]"
        }
      }
    }
  ]
}
Patient 資源：存儲與患者有關的信息，如姓名、性別和出生日期。
Observation 資源：
視力 (Visual Acuity) 觀察使用了 LOINC 代碼 "29544-3"，這是標準視力測量代碼。
眼內壓 (Intraocular Pressure, IOP) 觀察使用了 LOINC 代碼 "17864-0"，表示眼壓測量結果。
Bundle 資源：整合 Patient 和 Observation 資源，形成一個可以傳輸的資料集。
這樣的結構可以被任何支持 FHIR 的系統讀取，並且與其他醫療數據一起進行處理或交換。
