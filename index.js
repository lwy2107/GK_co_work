const express = require('express');
const mysql = require('mysql2/promise');

const app = express();
const port = 3000;

const connection = mysql.createPool({
  host: '20.69.222.136',
  user: 'root',
  password: 'test',
  database: 'mydb',
  prot: '3306',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

app.use(express.json());

app.post("/messages", async (req, res) => {
  let transaction;
  try {
    const message = req.body.message;
    const decodedMessage = decodeMessage(message);

    // Header 데이터 저장
    const headerQuery = `INSERT INTO header (house_id, boat_id, sensor_count) VALUES (?, ?, ?)`;
    const headerValues = [decodedMessage.houseId, decodedMessage.boatId, decodedMessage.sensorData.length];

    transaction = await connection.beginTransaction();
    await connection.query(headerQuery, headerValues, transaction);

    // 센서 데이터 저장
    await Promise.all(decodedMessage.sensorData.map(sensorData => saveSensorDataToDatabase(sensorData, transaction)));

    await transaction.commit();

    res.status(200).send("Message processed successfully");
  } catch (error) {
    console.error(error);
    if (transaction) {
      await transaction.rollback();
    }
    res.status(500).send("Internal Server Error: " + error.message);
  }
});

async function saveSensorDataToDatabase(sensorData, transaction) {
  const sensorType = sensorData.sensorType;
  const sensorValue = sensorData.sensorValue;

  switch (sensorType) {
    case 1:
      await saveSensorValueToDatabase('boat_lat', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
      break;
    case 2:
      await saveSensorValueToDatabase('boat_lon', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
      // Add more cases for other sensor types if needed
    case 3:
      await saveSensorValueToDatabase('acc_x', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);  
      break;
    case 4:
      await saveSensorValueToDatabase('acc_y', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
      break;
    case 5:
      await saveSensorValueToDatabase('acc_z', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
    case 6:
      await saveSensorValueToDatabase('ang_x', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);  
      break;
    case 7:
      await saveSensorValueToDatabase('ang_y', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
      break;
    case 8:
      await saveSensorValueToDatabase('ang_z', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
      break;
    case 9:
      await saveSensorValueToDatabase('degr_x', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);  
      break;
    case 10:
      await saveSensorValueToDatabase('degr_y', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
      break;
    case 11:
      await saveSensorValueToDatabase('degr_z', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
      break;
    case 12:
      await saveSensorValueToDatabase('mag_x', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);  
      break;
    case 13:
      await saveSensorValueToDatabase('mag_y', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
      break;
    case 14:
      await saveSensorValueToDatabase('mag_z', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
      break;        
    case 15:
      await saveSensorValueToDatabase('water_sen1', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);  
      break;
    case 16:
      await saveSensorValueToDatabase('water_sen2', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
      break;
    case 17:
      await saveSensorValueToDatabase('rpm', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
      break;
    case 18:
      await saveSensorValueToDatabase('battery', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);  
      break;
    case 19:
      await saveSensorValueToDatabase('dir_data', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
      break;
    case 20:
      await saveSensorValueToDatabase('dir_start', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);
      break;        // Add more cases for other sensor types if needed
    case 21:
      await saveSensorValueToDatabase('dir_end', sensorValue, sensorData.houseId, sensorData.boatId, sensorData.sensor_cent, transaction);  
      break;
    default:
      throw new Error(`Unsupported sensor type: ${sensorType}`);
  }
}

async function saveSensorValueToDatabase(column, sensorValue, houseId, boatId, sensorCent, transaction) {
  const sensorValueFloat = Buffer.from(sensorValue).readFloatLE(0);

  const query = `INSERT INTO sensors (house_id, boat_id, sensor_cent, ${column}) VALUES (?, ?, ?, ?)`;
  const values = [houseId, boatId, sensorCent, sensorValueFloat];

  await transaction.query(query, values);
}

function decodeMessage(message) {
  // 데이터 파싱 로직
  const houseId = message[0];
  const boatId = message[1];
  const sensorCent = message[2];

  const sensorData = [];
  for (let i = 3; i < message.length; i += 5) {
    const sensorType = message[i];
    const sensorValue = message.slice(i + 1, i + 5); // Assuming 4 bytes for sensor value
    sensorData.push({ sensorType, sensorValue, houseId, boatId, sensorCent });
  }

  return {
    houseId,
    boatId,
    sensor_cent: sensorCent,
    sensorData,
  };
}

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
