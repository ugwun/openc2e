#include "openc2e/VoiceData.h"
#include "openc2e/Catalogue.h"
#include "common/Exception.h"
#include <gtest/gtest.h>

class VoiceDataTest : public ::testing::Test {
protected:
    void SetUp() override {
        catalogue.reset();
    }

    void TearDown() override {
        catalogue.reset();
    }
};

TEST_F(VoiceDataTest, BasicParsing) {
    // Setup a valid DefaultLanguage tag with 81 hex values
    std::vector<std::string> langData;
    for (int i = 0; i < 81; ++i) {
        langData.push_back("1234ABCD");
    }
    catalogue.data["DefaultLanguage"] = langData;

    // Setup a valid Voice tag
    // 1 lang tag name + 32 pairs of (name, delay) = 65 entries
    std::vector<std::string> voiceData;
    voiceData.push_back("DefaultLanguage");
    for (int i = 0; i < 32; ++i) {
        voiceData.push_back("voice" + std::to_string(i));
        voiceData.push_back("10");
    }
    catalogue.data["TestVoice"] = voiceData;

    VoiceData vd("TestVoice");
    EXPECT_TRUE((bool)vd);
}

TEST_F(VoiceDataTest, InvalidHexThrows) {
    std::vector<std::string> langData;
    for (int i = 0; i < 80; ++i) {
        langData.push_back("1234ABCD");
    }
    langData.push_back("INVALID_HEX");
    catalogue.data["DefaultLanguage"] = langData;

    std::vector<std::string> voiceData;
    voiceData.push_back("DefaultLanguage");
    for (int i = 0; i < 32; ++i) {
        voiceData.push_back("v"); voiceData.push_back("0");
    }
    catalogue.data["TestVoice"] = voiceData;

    // std::stoul should throw std::invalid_argument or std::out_of_range
    EXPECT_ANY_THROW(VoiceData vd("TestVoice"));
}

TEST_F(VoiceDataTest, LargeHexValue) {
    std::vector<std::string> langData;
    for (int i = 0; i < 80; ++i) {
        langData.push_back("1");
    }
    // A value larger than 32-bit but fits in 64-bit unsigned long
    // stoul returns unsigned long. On 64-bit Windows, unsigned long is 32-bit!
    // Wait, on Windows 64-bit, unsigned long is still 32-bit (LLP64).
    // Let's use a value that definitely overflows 32-bit.
    langData.push_back("FFFFFFFFF"); // 9 Fs
    catalogue.data["DefaultLanguage"] = langData;

    std::vector<std::string> voiceData;
    voiceData.push_back("DefaultLanguage");
    for (int i = 0; i < 32; ++i) {
        voiceData.push_back("v"); voiceData.push_back("0");
    }
    catalogue.data["TestVoice"] = voiceData;

    // stoul or numeric_cast should throw
    // On Windows, stoul with 9 F's will likely return 0xFFFFFFFF and NOT throw? 
    // No, stoul throws out_of_range if the value is outside the range of unsigned long.
    // On Windows, unsigned long is 32-bit. So 9 F's should throw.
    EXPECT_ANY_THROW(VoiceData vd("TestVoice"));
}

TEST_F(VoiceDataTest, IncorrectLookupSizeThrows) {
    std::vector<std::string> langData(80, "1"); // 80 instead of 81
    catalogue.data["DefaultLanguage"] = langData;

    std::vector<std::string> voiceData;
    voiceData.push_back("DefaultLanguage");
    for (int i = 0; i < 32; ++i) {
        voiceData.push_back("v"); voiceData.push_back("0");
    }
    catalogue.data["TestVoice"] = voiceData;

    EXPECT_THROW(VoiceData vd("TestVoice"), Exception);
}

TEST_F(VoiceDataTest, IncorrectVoiceSizeThrows) {
    std::vector<std::string> langData(81, "1");
    catalogue.data["DefaultLanguage"] = langData;

    std::vector<std::string> voiceData;
    voiceData.push_back("DefaultLanguage");
    for (int i = 0; i < 31; ++i) { // 31 instead of 32
        voiceData.push_back("v"); voiceData.push_back("0");
    }
    catalogue.data["TestVoice"] = voiceData;

    EXPECT_THROW(VoiceData vd("TestVoice"), Exception);
}
