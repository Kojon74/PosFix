import React, { useState } from "react";
import { StyleSheet, View } from "react-native";
import Button from "./Button";
import { Colors } from "../../../styles";

const PostureScreen = () => {
  const [deviceConnected, setDeviceConnected] = useState(false);

  const calibrate = () => {};

  const startTimer = () => {};

  return (
    <View style={styles.container}>
      {deviceConnected ? (
        <View style={styles.homeBtnContainer}>
          <Button text="Calibrate" primary={false} handlePress={calibrate} />
          <Button text="Start" primary={true} handlePress={startTimer} />
        </View>
      ) : (
        <Button
          text="Connect"
          primary={false}
          handlePress={setDeviceConnected}
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
  homeBtnContainer: {
    height: "20%",
    justifyContent: "space-between",
  },
});
