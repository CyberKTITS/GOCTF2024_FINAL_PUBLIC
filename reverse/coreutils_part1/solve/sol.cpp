#pragma GCC target("avx2")
#pragma GCC optimize("O3,unroll-loops")
#include <bits/stdc++.h>
using namespace std;
#define ull unsigned long long

int main(){
    string txt = "kk{azummuihss_uyaykaaaCUv__pnaF\nei_t_a_aC_vthUaFgntesymuTaky_a}n_ytht{gzUrhC_g_}aCCTym__zayatevUmsC_\n{\n_ahryyehrgha_ku_e_pa{ahhs_iataa_eF_a_ihrerkveaFnUa_he_au{ee__r_i_Uua}aUiFhT{_{ea_\nFaaai{taeUa_kptzzm}aCamTpti_uypt_{TesrF\niTi_iiaCCnaaizvvheea__}}}\nCprF_s_maiC\neah_aasuse}F_}uaus_uzrt}_tpUi__}_t_v\nF_a_FtkTz{_CeamhCUCniiFniCr{e\nF{{tnitts_kaisiCtipnFtFita_uya_C_zn__hTsTpm_za_hevU{_hu{Fys_pe_yrt_r_a_m_ataCUmT_CU_hFk}Cr}pa}kUmF_a_szrah_as}vs}aa_enyeaehT_zs_vn_i_tUzgh___Faae\npah__gttUiU\niee_sa_tCha_zhg}mz_t__nu";
    vector<int> lens = {0,8192, 8192, 8190, 8192, 8190, 8190, 8190, 8192, 8190, 8190, 8184, 8184, 8190, 8190, 8190, 8192, 8177, 8190, 8189, 8180, 8190, 8184, 8188, 8184, 8175, 8190, 8181, 8176, 8178, 8190, 8184, 8192, 8184, 8160, 8190, 8172, 8177, 8170, 8190, 8160, 8159, 8190, 8170, 8184, 8190, 8188, 8178, 8160, 8183, 8150, 8160, 8164, 8162, 8154, 8140, 8176, 8151, 8178, 8142, 8160, 8174, 8184, 8190, 8192, 8190, 8184, 8174, 8160, 8142, 8190, 8165, 8136, 8176, 8140, 8175, 8132, 8162, 8190, 8137, 8160, 8181, 8118, 8134, 8148, 8160, 8170, 8178, 8184, 8188, 8190, 8190, 8188, 8184, 8178, 8170, 8160, 8148, 8134, 8118, 8100};
    for (int seed=0;seed<256;seed++){
        srand(seed);
        vector<int> arr;
        vector<int> newlines;
        for (int i=0;i<512;i++){ // len(txt)
            arr.push_back(rand());
            if (txt[i]=='\n'){
                newlines.push_back(arr[i]);
            }
        }
        for (int flag_len=5; flag_len<100;flag_len++){
            int r =1;
            for (auto x : newlines){
                if ((x%lens[flag_len])%flag_len != flag_len-1){
                    r= 0;
                    break;
                }
            }
            if (!r){
                continue;
            }
            cout << "FOUND LEN " << flag_len << '\n';
            char result[flag_len+1];
            for (int j=0;j<flag_len;j++)result[j]='?'; // этого символа явно нет в выведенном тексте
            
            for(int j=0;j<512;j++){
                if (result[(arr[j]%lens[flag_len]) % flag_len]=='?')
                    result[(arr[j]%lens[flag_len]) % flag_len] = txt[j];
                else if (result[(arr[j]%lens[flag_len]) % flag_len]!=txt[j]){
                    r = 0;
                    break;
                }
            }
            if (r){
                cout << "FOUND FLAG " << result << '\n'; 
            }
        }
    }
}