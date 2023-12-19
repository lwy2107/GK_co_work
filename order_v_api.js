const express = require('express');
const app = express();

app.use(express.json());

app.post('/api/data', (req, res) => {
  // JSON 메시지가 포함되어 있는지 확인합니다.
  if (!req.body) {
    res.status(400).send('JSON 메시지가 없습니다.');
    return;
  }

  // JSON 메시지를 파싱합니다.
  const data = req.body.message;

  // 메시지를 디코딩합니다.
  const decodedData = decodeData(data);

  // 디코딩된 데이터를 데이터베이스에 저장합니다.
  for (const set of decodedData) {
    processSet(set);
  }

  res.sendStatus(200);
});

// 각 세트를 처리합니다.
function processSet(setData) {
  // 센서 데이터의 세트를 처리하는 로직을 추가합니다.
  const houseId = parseInt(setData.substr(2, 2), 16);
  const boatId = parseInt(setData.substr(4, 2), 16);
  const sensorCent = parseInt(setData.substr(6, 2), 16);

  console.log(`House ID: ${houseId}, Boat ID: ${boatId}, Sensor Cent: ${sensorCent}`);

  // 센서 데이터를 파싱합니다.
  for (let i = 8; i < setData.length; i += 8) {
    const sensorType = parseInt(setData.substr(i, 2), 16);
    const sensorValueHex = setData.substr(i + 2, 6);
    const sensorValueFloat = Buffer.from(sensorValueHex, 'hex').readFloatLE(0);

    console.log(`Sensor Type: ${sensorType}, Sensor Value: ${sensorValueFloat}`);
  }
}

// 메시지를 디코딩합니다.
function decodeData(data) {
  const sets = [];
  let startIdx = 0;

  while (startIdx < data.length) {
    // 세트의 시작 부분을 찾습니다.
    const startMarker = data.indexOf('24010101', startIdx);

    if (startMarker === -1) {
      // 세트의 시작 부분이 더 이상 없으면 종료합니다.
      break;
    }

    // 세트의 시작 부분 이후의 데이터를 가져옵니다.
    const setData = data.slice(startMarker, startMarker + 32);

    // 세트 데이터를 처리합니다.
    processSet(setData);

    // 다음 세트를 찾기 위해 시작 인덱스를 조정합니다.
    startIdx = startMarker + 32;
  }

  return sets;
}

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
