package hellocucumber;
import org.apache.http.Header;
import org.apache.http.HttpEntity;
import org.apache.http.HttpHeaders;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.json.*;
import java.io.IOException;
import java.util.List;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.Assert.*;

public class StepDefinitions {

    ////FOR ID_004 View My Profile
    private int user_id;
    private String name;
    private String email;
    private String descr;
    private String pswd;
    private String err;

    @Given("I am logged in as an user with id=20")
    public void i_am_logged_in_as_an_user_with_id_20() {
        user_id = 20;
    }

    @When("I view my profile")
    public void i_view_my_profile() throws Exception {
        CloseableHttpClient httpClient = HttpClients.createDefault();

        // Write code here that turns the phrase above into concrete actions
        HttpGet request = new HttpGet("https://were-board.herokuapp.com/user/profile/"+Integer.toString(user_id));

        try (CloseableHttpResponse response = httpClient.execute(request)) {

            HttpEntity entity = response.getEntity();

            if (entity != null) {

                // return it as a String
                String result = EntityUtils.toString(entity);
                JSONObject obj = new JSONObject(result);
                if (obj.has("error")){
                    err = obj.getString("error");//obj.getString("error");
                }
                else {
                    name = obj.getString("name");
                    email = obj.getString("email");
                    descr = obj.getString("description");
                    pswd = obj.getString("password");
                }
            }

        }

    }

    @Then("the system displays the following:")
    public void the_system_displays_the_following(io.cucumber.datatable.DataTable dataTable) {
        // Write code here that turns the phrase above into concrete actions
        // For automatic transformation, change DataTable to one of
        // E, List<E>, List<List<E>>, List<Map<K,V>>, Map<K,V> or
        // Map<K, List<V>>. E,K,V must be a String, Integer, Float,
        // Double, Byte, Short, Long, BigInteger or BigDecimal.
        //
        // For other transformations you can register a DataTableType.
        List list =  dataTable.asList();
        assertEquals(list.get(5+0), Integer.toString(user_id));
        assertEquals(list.get(5+1), name);
        assertEquals(list.get(5+2), email);
        assertEquals(list.get(5+3), descr);
        assertEquals(list.get(5+4), pswd);
    }

    @Given("my account is deleted")
    public void my_account_is_deleted() {
        // Write code here that turns the phrase above into concrete actions
        user_id = -1;
    }


    @Then("the system displays an {string} error message")
    public void the_system_displays_an_error_message(String string) {
        // Write code here that turns the phrase above into concrete actions
        assertEquals(string, err);

    }


}
