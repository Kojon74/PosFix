import React from "react";
import { StyleSheet, Text, View, Image } from "react-native";
import { Colors } from "../../../styles";

const ProfileScreen = () => {
  return (
    <View style={styles.container}>
      <Image source={require("../../../assets/profile.png")} alt="Profile" />
    </View>
  );
};

export default ProfileScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.SECONDARY,
    alignItems: "center",
    justifyContent: "center",
  },
});
