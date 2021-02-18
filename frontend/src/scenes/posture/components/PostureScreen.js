import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { Colors } from "_styles";

const PostureScreen = () => {
  return (
    <View style={styles.container}>
      <Text>Home</Text>
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
