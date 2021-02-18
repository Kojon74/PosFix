import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { Colors } from "_styles";

const DailyScreen = () => {
  const name = "ken";
  return (
    <View style={styles.container}>
      <Text>Daily</Text>
    </View>
  );
};

export default DailyScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.SECONDARY,
    alignItems: "center",
    justifyContent: "center",
  },
});
