import React, { useState } from "react";
import { StyleSheet, View } from "react-native";
import Button from "./Button";
import { Colors } from "../../../styles";
import CalibrateStartBtn from "./CalibrateStartBtn";
import CalibrateInstr from "./CalibrateInstr";
import Stopwatch from "./Stopwatch";
import { useGlobalContext } from "../../../../context";

const PostureScreen = ({ navigation }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [isCalbrating, setIsCalibrating] = useState(false);
  const [isStarted, setIsStarted] = useState(false);

  const { startStopwatch } = useGlobalContext();

  const calibrate = () => {
    setIsCalibrating(true);
  };

  const startTimer = () => {
    startStopwatch();
    setIsStarted(true);
  };

  const handleIsConnected = () => {
    setIsConnected(true);
  };

  return (
    <View style={styles.container}>
      {isConnected && !isCalbrating && !isStarted ? (
        <CalibrateStartBtn calibrate={calibrate} startTimer={startTimer} />
      ) : isConnected && isCalbrating ? (
        <CalibrateInstr setIsCalibrating={setIsCalibrating} />
      ) : isConnected && isStarted ? (
        <Stopwatch navigation={navigation} setIsStarted={setIsStarted} />
      ) : (
        <Button
          text="Connect"
          primary={false}
          handlePress={handleIsConnected}
        />
      )}
    </View>
  );
};

export default PostureScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.SECONDARY,
    alignItems: "center",
    justifyContent: "center",
  },
});
