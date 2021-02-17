import React from "react";
import { StyleSheet, Text, View } from "react-native";

const DailyScreen = () => {
  return (
    <View style={styles.container}>
      <Text>Daily</Text>
    </View>
  );
};

export default DailyScreen;

const colors = { primary: "#05386B", secondary: "#5CDB95" };

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.secondary,
    alignItems: "center",
    justifyContent: "center",
  },
});
